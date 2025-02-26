import asyncio
import collections
import logging
import threading
import time
import traceback

import cv2
import numpy as np
import pyglet
from pipecat.frames.frames import (
    EndFrame,
    Frame,
    InputAudioRawFrame,
    OutputImageRawFrame,
    StartFrame,
)
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor
from pipecat.transports.base_input import BaseInputTransport
from pipecat.transports.base_output import BaseOutputTransport
from pipecat.transports.base_transport import TransportParams

from .media_consumer import MediaConsumer


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


class PipecatAudioTransportParams(TransportParams):
    sink_name: str = "steam"


class PipecatAudioOutputTransport(BaseOutputTransport):
    """A transport that sends audio data to a specified sink using GStreamer.

    This transport uses GStreamer to send audio data to a specified sink,
    such as a PulseAudio device. It handles the setup and management of the
    GStreamer pipeline for audio output.
    """

    _gst_initialized = False
    _init_lock = threading.Lock()
    Gst = None

    @classmethod
    def _initialize_gstreamer(cls):
        """Initialize GStreamer once for all instances."""
        if not cls._gst_initialized:
            with cls._init_lock:
                if not cls._gst_initialized:  # Double-check pattern
                    try:
                        import gi

                        gi.require_version("Gst", "1.0")
                        from gi.repository import Gst

                        cls.Gst = Gst
                        Gst.init(None)
                        cls._gst_initialized = True
                    except (ImportError, ValueError) as e:
                        raise RuntimeError(
                            "GStreamer dependencies not found. Please install gstreamer and gi packages."
                        ) from e

    def __init__(self, params: PipecatAudioTransportParams, **kwargs):
        super().__init__(params, **kwargs)
        self._initialize_gstreamer()

        self.frame_buffer = collections.deque()
        self.running = False
        self.pipeline = self.Gst.parse_launch(
            f"appsrc name=audio_src format=time ! "
            f"audio/x-raw,format=S16LE,rate={self._params.audio_out_sample_rate},channels={self._params.audio_out_channels} ! "
            f"pulsesink device={params.sink_name}"
        )
        self.appsrc = self.pipeline.get_by_name("audio_src")
        self.appsrc.set_property("format", self.Gst.Format.TIME)
        self.appsrc.set_property("blocksize", 4096)

    async def write_raw_audio_frames(self, frames: bytes):
        """Push audio frames into PipeWire using GStreamer"""
        buf = self.Gst.Buffer.new_allocate(None, len(frames), None)
        buf.fill(0, frames)
        self.appsrc.emit("push-buffer", buf)
        self.frame_buffer.append(frames)

    async def start(self, frame: StartFrame):
        """Start playback by consuming frames from buffer"""
        await super().start(frame)
        if self.running:
            return  # Avoid restarting if already running

        self.running = True
        self.pipeline.set_state(self.Gst.State.PLAYING)

    def _push_frames(self):
        """Push frames from buffer into GStreamer pipeline"""
        if not self.running:
            return False  # Stop loop if playback is stopped

        if self.frame_buffer:
            frames = self.frame_buffer.popleft()  # Get next frame
            buf = self.Gst.Buffer.new_allocate(None, len(frames), None)
            buf.fill(0, frames)
            self.appsrc.emit("push-buffer", buf)

        # Keep calling until buffer is empty
        return True if self.running else False

    async def stop(self, frame: EndFrame):
        """Stop playback and clear buffer"""
        await super().stop(frame)
        self.running = False
        self.pipeline.set_state(self.Gst.State.NULL)
        self.frame_buffer.clear()


class PipecatAudioInputTransport(BaseInputTransport):
    def __init__(self, params: TransportParams, config: dict):
        super().__init__(params)

        self.chunk_size = config.get("chunk_size", 1024)
        self.chunk_delay = config.get("chunk_delay", 0.05)
        self._num_channels = params.audio_in_channels
        self.mic_id = config.get("mic_id", None)
        self._running = False
        self._wave_file = None
        self._last_chunk_time = 0
        self.consumer = MediaConsumer(
            audio_node_id=self.mic_id, audio_sample_rate=params.audio_in_sample_rate
        )
        self.consumer.push_handlers(data=self._media_consumer_frame_handler)

    async def start(self, frame):
        if self.consumer.audio_pipeline:
            return
        self.consumer.start()
        await super().start(frame)

    async def stop(self, frame):
        self.consumer.stop()
        await super().stop(frame)

    def _media_consumer_frame_handler(self, frame):
        if frame.type == "audio":
            chunk = frame.data.tobytes()
            audio_raw_frame = InputAudioRawFrame(
                audio=chunk,
                sample_rate=self.consumer.audio_sample_rate,
                num_channels=self.consumer.audio_channels,
            )
            asyncio.run_coroutine_threadsafe(
                self.push_audio_frame(audio_raw_frame), self.get_event_loop()
            )
            print(f"Pushed audio frame: {audio_raw_frame}")
