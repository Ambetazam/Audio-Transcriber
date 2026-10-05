from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .transcriber import TranscriptionResult


def format_timestamp(seconds: float) -> str:
    """Format seconds as HH:MM:SS.mmm."""

    milliseconds = round(seconds * 1000)
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1_000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def to_txt(result: TranscriptionResult, timestamps: bool = True) -> str:
    if not timestamps:
        return result.text + "\n"

    lines = [
        f"Source: {result.source.name}",
        f"Language: {result.language} ({result.language_probability:.2%} confidence)",
        "",
    ]
    lines.extend(
        f"[{format_timestamp(segment.start)} --> {format_timestamp(segment.end)}] {segment.text}"
        for segment in result.segments
    )
    return "\n".join(lines).rstrip() + "\n"


def to_markdown(result: TranscriptionResult, *, timestamps: bool = True) -> str:
    generated = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    lines = [
        f"# Transcription — {result.source.name}",
        "",
        "> Generated locally with `audio-transcriber` / `faster-whisper`.",
        "> Review the transcript before using it as formal evidence.",
        "",
        "## Metadata",
        "",
        f"- **Source:** `{result.source.name}`",
        f"- **Language:** `{result.language}`",
        f"- **Detection confidence:** `{result.language_probability:.2%}`",
        f"- **Generated:** `{generated}`",
        "",
        "## Transcript",
        "",
    ]

    if timestamps:
        lines.extend(
            f"**[{format_timestamp(segment.start)} → {format_timestamp(segment.end)}]** {segment.text}"
            for segment in result.segments
        )
    else:
        lines.append(result.text)

    return "\n".join(lines).rstrip() + "\n"


def write_output(
    result: TranscriptionResult,
    output_dir: str | Path,
    fmt: str,
    *,
    timestamps: bool = True,
) -> Path:
    target_dir = Path(output_dir).expanduser()
    target_dir.mkdir(parents=True, exist_ok=True)

    if fmt == "txt":
        target = target_dir / f"{result.source.stem}.txt"
        target.write_text(to_txt(result, timestamps=timestamps), encoding="utf-8")
    elif fmt == "md":
        target = target_dir / f"{result.source.stem}.md"
        target.write_text(to_markdown(result, timestamps=timestamps), encoding="utf-8")
    else:
        raise ValueError("format must be 'txt' or 'md'")

    return target
