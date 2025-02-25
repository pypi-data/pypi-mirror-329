import asyncio
import logging
import time
import traceback

import cv2
import numpy as np
import pyglet
from pipecat.frames.frames import EndFrame, Frame, OutputImageRawFrame, StartFrame
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor


class PipecatVideoOutputProcessor(FrameProcessor):
    """A frame processor that displays video frames in a Pyglet window.

    This processor takes video frames and displays them in real-time using
    a Pyglet window. It handles frame rate timing and image conversion from
    BGR to RGB format.

    Args:
        config (dict): Configuration dictionary with the following optional keys:
            - frame_rate (int): Target frame rate in FPS (default: 30)
            - width (int): Window width in pixels (default: 1920)
            - height (int): Window height in pixels (default: 1080)
    """

    def __init__(self, config: dict):
        super().__init__()

        self.frame_rate = config.get("frame_rate", 30)
        self.width = config.get("width", 1920)
        self.height = config.get("height", 1080)
        self.img: pyglet.image.ImageData | None = None
        self.window = pyglet.window.Window(
            self.width, self.height, resizable=False, fullscreen=False
        )
        self.logger = logging.getLogger(__name__)

    async def start(self, frame: StartFrame):
        """Initialize the display window and start the update loop.

        Args:
            frame (StartFrame): The start frame triggering initialization
        """
        self.measured_frame_time = time.time()
        self.update_window_task = self.create_task(self._update_window())
        pass

    async def stop(self, frame: EndFrame):
        """Clean up resources when stopping the processor.

        Args:
            frame (EndFrame): The end frame triggering cleanup
        """
        if hasattr(self, "update_window_task"):
            self.update_window_task.cancel()
        pass

    async def _update_window(self):
        """Background task that updates the Pyglet window at the target frame rate.

        This method runs continuously, managing the timing of frame updates and
        rendering the current image to the window.
        """
        frame_time = 1.0 / self.frame_rate  # Time per frame in seconds
        last_frame_time = time.time()

        while True:  # Run continuously
            current_time = time.time()
            # Check if it's time for the next frame
            if current_time - last_frame_time < frame_time:
                await asyncio.sleep(0.001)  # Small sleep to prevent CPU spinning
                continue

            self.window.switch_to()
            self.window.clear()
            if self.img is not None:
                self.img.blit(0, 0, 0, self.width, self.height)

            self.window.flip()
            last_frame_time = current_time

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        """Process incoming frames and route them to appropriate handlers.

        Args:
            frame (Frame): The frame to process
            direction (FrameDirection): The direction the frame is traveling

        Routes StartFrame, EndFrame and OutputImageRawFrame types to their
        respective handlers.
        """
        await super().process_frame(frame, direction)

        if isinstance(frame, StartFrame):
            await self.start(frame)
        elif isinstance(frame, EndFrame):
            await self.stop(frame)
        elif isinstance(frame, OutputImageRawFrame):
            await self.process_video_frame(frame)

        await self.push_frame(frame, direction)

    async def process_video_frame(self, frame: OutputImageRawFrame) -> None:
        """Process a video frame for display.

        Args:
            frame (OutputImageRawFrame): Frame containing JPEG image data

        Decodes the JPEG image data, converts it to RGB format, and prepares it
        for display in the Pyglet window.
        """
        # Decode JPEG frame
        try:
            img = cv2.imdecode(np.frombuffer(frame.image, np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                self.logger.error("Failed to decode video frame")
                return

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.flip(img, 0)  # Flip vertically for pyglet

            # Create ImageData with the correct dimensions and raw RGB data
            self.img = pyglet.image.ImageData(self.width, self.height, "RGB", img.tobytes())
        except Exception as e:
            self.logger.error(f"Error processing video frame: {e}")
            traceback.print_exc()
