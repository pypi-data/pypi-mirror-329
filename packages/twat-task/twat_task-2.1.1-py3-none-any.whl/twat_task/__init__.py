"""
twat_task - Video processing task utilities using Prefect for workflow management.

This package provides a set of tasks and flows for processing video files,
including audio extraction and transcription. It uses Prefect for workflow
management and Pydantic for data validation.

Example:
    >>> from twat_task import VideoTranscript
    >>> from pathlib import Path
    >>>
    >>> # Process a video file
    >>> vt = VideoTranscript(video_path=Path("video.mp4"))
    >>> print(vt.audio_path)  # Extracts audio
    >>> print(vt.text_transcript)  # Generates transcript
"""

from importlib import metadata

from twat_task.__version__ import version as __version__
from twat_task.task import (
    VideoTranscript,
    extract_audio_task,
    generate_transcript_task,
    process_video_flow,
)

__all__ = [
    "VideoTranscript",
    "__version__",
    "extract_audio_task",
    "generate_transcript_task",
    "process_video_flow",
]
