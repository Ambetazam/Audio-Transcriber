from pathlib import Path

from audio_transcriber.formatters import format_timestamp, to_txt
from audio_transcriber.transcriber import Segment, TranscriptionResult


def sample_result() -> TranscriptionResult:
    return TranscriptionResult(
        source=Path("example.m4a"),
        language="es",
        language_probability=0.98,
        segments=(
            Segment(0.0, 2.5, "Hola, ¿cómo estás?"),
            Segment(2.5, 5.125, "Este es un ejemplo."),
        ),
    )


def test_format_timestamp() -> None:
    assert format_timestamp(3723.125) == "01:02:03.125"


def test_txt_contains_timestamps() -> None:
    output = to_txt(sample_result())
    assert "[00:00:00.000 --> 00:00:02.500] Hola, ¿cómo estás?" in output
    assert "Language: es" in output
