#!/usr/bin/env python3
import threading
import traceback
from queue import Queue
from threading import Event

import cv2
import depthai as dai
import numpy as np

from hivebox.common import ConfigWrapper, select_device, wait_for_device

class VideoSaver(threading.Thread):
    _worker_q = Queue(maxsize=10)
    _running = Event()

    def __init__(self, output_path: str):
        super().__init__()
        self._output_path = output_path

    # NOTE: Use start() to start the thread, this method is a new thread starting point
    def run(self):
        self._running.set()
        print("Starting saver...")
        writer = None
        while self._running.is_set():
            try:
                if not self._worker_q.empty():
                    frame = self._worker_q.get()
                    if not writer:
                        writer = cv2.VideoWriter(self._output_path, cv2.VideoWriter_fourcc(*"mp4v"), 30, (frame.shape[1], frame.shape[0]))
                    writer.write(frame)
            except:
                traceback.print_exc()
                break
        print("Terminating saver...")
        if writer:
            writer.release()

    def store_frame(self, frame):
        self._worker_q.put(frame)

    def stop(self):
        print('Saver stopping...')
        self._running.clear()

def create_pipeline(rgb_res, lrc, ext, sub):
    pipeline = dai.Pipeline()

    rgb = pipeline.create(dai.node.ColorCamera)
    left = pipeline.create(dai.node.MonoCamera)
    right = pipeline.create(dai.node.MonoCamera)
    depth = pipeline.create(dai.node.StereoDepth)
    xout_disp = pipeline.create(dai.node.XLinkOut)
    xout_rgb = pipeline.create(dai.node.XLinkOut)

    rgb.setInterleaved(False)
    rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
    rgb.setResolution(rgb_res)
    rgb.setVideoNumFramesPool(10)

    xout_disp.setStreamName("disparity")
    xout_rgb.setStreamName("color")

    left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)
    left.setCamera("left")
    right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)
    right.setCamera("right")

    depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_3x3)
    depth.setDepthAlign(dai.CameraBoardSocket.CAM_A)
    depth.setLeftRightCheck(lrc)
    depth.setExtendedDisparity(ext)
    depth.setSubpixel(sub)

    # Script node will sync high-res frames
    script = pipeline.create(dai.node.Script)

    # Send both streams to the Script node so we can sync them
    depth.disparity.link(script.inputs["disp_in"])
    rgb.video.link(script.inputs["rgb_in"])

    script.setScript("""
        FPS=30
        import time
        from datetime import timedelta
        import math

        # Timestamp threshold (in miliseconds) under which frames will be considered synced.
        # Lower number means frames will have less delay between them, which can potentially
        # lead to dropped frames.
        MS_THRESHOL=math.ceil(500 / FPS)

        def check_sync(queues, timestamp):
            matching_frames = []
            for name, list in queues.items(): # Go through each available stream
                # node.warn(f"List {name}, len {str(len(list))}")
                for i, msg in enumerate(list): # Go through each frame of this stream
                    time_diff = abs(msg.getTimestamp() - timestamp)
                    if time_diff <= timedelta(milliseconds=MS_THRESHOL): # If time diff is below threshold, this frame is considered in-sync
                        matching_frames.append(i) # Append the position of the synced frame, so we can later remove all older frames
                        break

            if len(matching_frames) == len(queues):
                # We have all frames synced. Remove the excess ones
                i = 0
                for name, list in queues.items():
                    queues[name] = queues[name][matching_frames[i]:] # Remove older (excess) frames
                    i+=1
                return True
            else:
                return False # We don't have synced frames yet

        names = ['disp', 'rgb']
        frames = dict() # Dict where we store all received frames
        for name in names:
            frames[name] = []

        while True:
            for name in names:
                f = node.io[name+"_in"].tryGet()
                if f is not None:
                    frames[name].append(f) # Save received frame

                    if check_sync(frames, f.getTimestamp()): # Check if we have any synced frames
                        # Frames synced!
                        node.info(f"Synced frame!")
                        # node.warn(f"Queue size. Disp: {len(frames['disp'])}, rgb: {len(frames['rgb'])}")
                        for name, list in frames.items():
                            syncedF = list.pop(0) # We have removed older (excess) frames, so at positions 0 in dict we have synced frames
                            node.info(f"{name}, ts: {str(syncedF.getTimestamp())}, seq {str(syncedF.getSequenceNum())}")
                            node.io[name+'_out'].send(syncedF) # Send synced frames to the host


            time.sleep(0.001)  # Avoid lazy looping
    """)

    script.outputs['disp_out'].link(xout_disp.input)
    script.outputs['rgb_out'].link(xout_rgb.input)

    # Linking
    left.out.link(depth.left)
    right.out.link(depth.right)

    return pipeline


def main():
    config = ConfigWrapper()
    config.check_udev_rules()

    device_info = select_device()
    with dai.Device(device_info) as device:
        usb_2 = config.is_usb2(device)
        resolution = config.get_resolution(device)
        ir_enabled = config.ir_enabled(device)

    found = wait_for_device(device_info.mxid)

    if not found:
        raise RuntimeError("Device not found after reboot!")
    pipeline = create_pipeline(
        rgb_res=resolution,
        lrc=config.args.stereoLrCheck,
        ext=config.args.extendedDisparity,
        sub=config.args.subpixel,
    )

    saver = VideoSaver('out.mp4')
    saver.start()

    with dai.Device(pipeline, maxUsbSpeed=dai.UsbSpeed.HIGH if usb_2 else dai.UsbSpeed.SUPER_PLUS) as device:
        if ir_enabled:
            device.setIrLaserDotProjectorIntensity(1)

        q_disp = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)
        q_rgb = device.getOutputQueue(name="color", maxSize=4, blocking=False)
        while True:
            try:

                rgb_packet = q_rgb.get()
                disp_packet = q_disp.get()
                rgb_frame = rgb_packet.getCvFrame()
                disp_frame = disp_packet.getCvFrame()
                disp_frame = (disp_frame * (255 / config.max_disparity)).astype(np.uint8)
                disp_frame = cv2.applyColorMap(disp_frame, cv2.COLORMAP_JET)
                combined = np.concatenate((rgb_frame, disp_frame), axis=0)
                saver.store_frame(combined)
            except KeyboardInterrupt:
                print("Terminating...")
                saver.stop()
                break

if __name__ == '__main__':
    main()
