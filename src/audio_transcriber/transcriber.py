from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from faster_whisper import WhisperModel

SUPPORTED_AUDIO_EXTENSIONS = {
    ".aac",
    ".flac",
    ".m4a",
    ".mp3",
    ".ogg",
    ".opus",
    ".wav",
    ".webm",
    ".wma",
}


@dataclass(frozen=True)
class Segment:
    """A single timestamped piece of transcription."""

    start: float
    end: float
    text: str


@dataclass(frozen=True)
class TranscriptionResult:
    """Complete transcription result and detected metadata."""

    source: Path
    language: str
    language_probability: float
    segments: tuple[Segment, ...]

    @property
    def text(self) -> str:
        return " ".join(segment.text.strip() for segment in self.segments).strip()


class AudioTranscriber:
    """Thin, reusable wrapper around faster-whisper."""

    def __init__(
        self,
        model_name: str = "small",
        device: str = "cpu",
        compute_type: str = "int8",
        cpu_threads: int | None = None,
        download_root: str | Path | None = None,
    ) -> None:
        kwargs: dict[str, object] = {
            "device": device,
            "compute_type": compute_type,
        }
        if cpu_threads is not None:
            kwargs["cpu_threads"] = cpu_threads
        if download_root is not None:
            kwargs["download_root"] = str(download_root)

        self.model = WhisperModel(model_name, **kwargs)

    def transcribe(
        self,
        source: str | Path,
        *,
        language: str | None = None,
        task: str = "transcribe",
        beam_size: int = 5,
        vad_filter: bool = True,
        word_timestamps: bool = False,
    ) -> TranscriptionResult:
        source_path = Path(source).expanduser().resolve()
        if not source_path.is_file():
            raise FileNotFoundError(f"Audio file not found: {source_path}")
        if source_path.suffix.lower() not in SUPPORTED_AUDIO_EXTENSIONS:
            supported = ", ".join(sorted(SUPPORTED_AUDIO_EXTENSIONS))
            raise ValueError(
                f"Unsupported audio format '{source_path.suffix}'. "
                f"Supported formats: {supported}"
            )
        if task not in {"transcribe", "translate"}:
            raise ValueError("task must be 'transcribe' or 'translate'")

        segments, info = self.model.transcribe(
            str(source_path),
            language=language,
            task=task,
            beam_size=beam_size,
            vad_filter=vad_filter,
            word_timestamps=word_timestamps,
        )

        collected = tuple(
            Segment(
                start=float(segment.start),
                end=float(segment.end),
                text=segment.text.strip(),
            )
            for segment in segments
            if segment.text and segment.text.strip()
        )

        return TranscriptionResult(
            source=source_path,
            language=info.language,
            language_probability=float(info.language_probability),
            segments=collected,
        )


def discover_audio_files(path: str | Path) -> list[Path]:
    """Return supported audio files from a file or directory, sorted by name."""

    root = Path(path).expanduser()
    if root.is_file():
        if root.suffix.lower() not in SUPPORTED_AUDIO_EXTENSIONS:
            raise ValueError(f"Unsupported audio format: {root.suffix}")
        return [root]

    if root.is_dir():
        return sorted(
            (file for file in root.rglob("*") if file.is_file() and file.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS),
            key=lambda file: str(file).lower(),
        )

    raise FileNotFoundError(f"Input path does not exist: {root}")
