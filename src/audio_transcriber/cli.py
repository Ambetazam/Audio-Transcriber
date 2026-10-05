from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .formatters import write_output
from .transcriber import AudioTranscriber, discover_audio_files


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="audio-transcriber",
        description="Transcribe local audio files with faster-whisper.",
    )
    parser.add_argument("input", help="Audio file or directory containing audio files")
    parser.add_argument(
        "--output-dir",
        default="transcripts",
        help="Directory where transcripts are written (default: transcripts)",
    )
    parser.add_argument(
        "--model",
        default="small",
        help="Whisper model: tiny, base, small, medium, large-v3, turbo, etc. (default: small)",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        choices=["cpu", "cuda", "auto"],
        help="Inference device (default: cpu)",
    )
    parser.add_argument(
        "--compute-type",
        default="int8",
        help="CTranslate2 compute type (default: int8)",
    )
    parser.add_argument("--language", default=None, help="Language code, e.g. es or en")
    parser.add_argument(
        "--task",
        default="transcribe",
        choices=["transcribe", "translate"],
        help="Transcribe in original language or translate to English",
    )
    parser.add_argument("--beam-size", type=int, default=5)
    parser.add_argument("--cpu-threads", type=int, default=None)
    parser.add_argument(
        "--format",
        dest="output_format",
        choices=["txt", "md"],
        default="md",
        help="Output format (default: md)",
    )
    parser.add_argument(
        "--no-timestamps",
        action="store_true",
        help="Write plain transcript text without timestamps",
    )
    parser.add_argument(
        "--no-vad",
        action="store_true",
        help="Disable voice activity detection",
    )
    parser.add_argument(
        "--word-timestamps",
        action="store_true",
        help="Request word-level timestamps from the model",
    )
    parser.add_argument("--version", action="version", version=__version__)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        files = discover_audio_files(args.input)
        if not files:
            print("No supported audio files found.", file=sys.stderr)
            return 1

        print(f"Found {len(files)} audio file(s).")
        print(f"Loading model '{args.model}' on {args.device}/{args.compute_type}...")
        transcriber = AudioTranscriber(
            model_name=args.model,
            device=args.device,
            compute_type=args.compute_type,
            cpu_threads=args.cpu_threads,
        )

        for index, audio_file in enumerate(files, start=1):
            print(f"\n[{index}/{len(files)}] {audio_file}")
            result = transcriber.transcribe(
                audio_file,
                language=args.language,
                task=args.task,
                beam_size=args.beam_size,
                vad_filter=not args.no_vad,
                word_timestamps=args.word_timestamps,
            )
            output = write_output(
                result,
                args.output_dir,
                args.output_format,
                timestamps=not args.no_timestamps,
            )
            print(
                f"Language: {result.language} "
                f"({result.language_probability:.1%})"
            )
            print(f"Written: {output}")

        print("\nTranscription complete.")
        return 0

    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
