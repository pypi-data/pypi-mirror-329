"""Core task functionality for video processing using Prefect."""

from __future__ import annotations

from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING

from prefect import flow, task
from pydantic import BaseModel, computed_field

if TYPE_CHECKING:
    from pathlib import Path


@task(retries=2)
def extract_audio_task(video_path: Path, audio_path: Path) -> None:
    """Extract audio from video, simulating a long-running process.

    Args:
        video_path: Path to the input video file
        audio_path: Path where the extracted audio should be saved
    """

    # Simulate fetching video metadata as JSON
    import json
    import time
    from random import randint

    time.sleep(2)  # Simulate API call

    metadata = {
        "duration": randint(60, 3600),
        "codec": "aac",
        "bitrate": f"{randint(128, 320)}kbps",
        "channels": 2,
        "sample_rate": 44100,
    }

    metadata["duration"] // 10
    for _i in range(10):
        time.sleep(0.5)  # Simulate processing time

    # Save simulated audio and metadata
    audio_path.write_text(json.dumps(metadata))


@task(retries=2)
def generate_transcript_task(audio_path: Path) -> str:
    """Generate transcript from audio, simulating API calls and processing.

    Args:
        audio_path: Path to the input audio file

    Returns:
        Generated transcript text
    """

    import json
    import time
    from random import choice, randint

    # Simulate loading audio metadata
    metadata = json.loads(audio_path.read_text())

    time.sleep(1.5)

    # Simulate processing chunks with progress
    duration = metadata["duration"]
    chunk_size = 30  # Process in 30-second chunks
    chunks = duration // chunk_size

    words = [
        "hello",
        "world",
        "this",
        "is",
        "a",
        "test",
        "video",
        "with",
        "some",
        "random",
        "words",
        "being",
        "processed",
    ]

    transcript_parts = []
    for _i in range(chunks):
        time.sleep(0.3)  # Simulate API call and processing
        # Generate some random text
        chunk_text = " ".join(choice(words) for _ in range(randint(5, 15)))
        transcript_parts.append(chunk_text)

    return " ".join(transcript_parts)


@flow
def process_video_flow(video_path: Path) -> tuple[Path, str]:
    """Process a video file to extract audio and generate transcript.

    Args:
        video_path: Path to the input video file

    Returns:
        Tuple containing:
        - Path to the extracted audio file
        - Generated transcript text
    """
    audio = video_path.with_suffix(".mp3")
    # Only extract audio if the file does not exist
    if not audio.exists():
        extract_audio_task(video_path, audio)
    transcript = generate_transcript_task(audio)
    return audio, transcript


class VideoTranscript(BaseModel):
    """Pydantic model for video transcription with computed fields.

    This model handles the video processing task, including audio extraction
    and transcript generation. The processing is done lazily when the computed
    fields are accessed.

    Attributes:
        video_path: Path to the input video file
        audio_path: Computed field containing path to extracted audio
        text_transcript: Computed field containing generated transcript
    """

    video_path: Path

    @computed_field
    @cached_property
    def audio_path(self) -> Path:
        """Get path to extracted audio file, processing video if needed."""
        audio, _ = process_video_flow(self.video_path)
        return audio

    @computed_field
    @cached_property
    def text_transcript(self) -> str:
        """Get transcript text, processing video and audio if needed."""
        _, transcript = process_video_flow(self.video_path)
        return transcript
