# Audio Transcriber

Local command-line transcription tool for turning **audio recordings into searchable text** using [faster-whisper](https://github.com/SYSTRAN/faster-whisper).

The project is designed especially for study/work evidence: conversations, meetings, interviews, class recordings, and other audio that needs to become a timestamped `.txt` or `.md` document.

> **Privacy principle:** audio files and generated transcripts are intentionally ignored by Git by default. Keep sensitive recordings on your local machine unless you explicitly decide otherwise.

## Features

- Transcribe one audio file or an entire directory.
- Spanish-friendly workflow with automatic language detection.
- Timestamped transcripts for evidence review.
- Plain `.txt` or structured `.md` output.
- CPU INT8 by default for a practical local setup.
- Optional CUDA execution for compatible NVIDIA systems.
- Voice Activity Detection (VAD) enabled by default.
- Optional word timestamps.
- No system FFmpeg installation is required by `faster-whisper`; decoding is handled through PyAV. See the upstream documentation for the current supported setup. 

## Project structure

```text
Audio-Transcriber/
├── src/
│   └── audio_transcriber/
│       ├── __init__.py
│       ├── cli.py
│       ├── formatters.py
│       └── transcriber.py
├── tests/
│   └── test_formatters.py
├── examples/
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

## Requirements

- Python 3.10+
- `pip`
- Enough RAM/storage for the Whisper model you choose

The first run downloads the selected model. The exact model size and resource requirements depend on the model chosen.

## Installation

Clone the repository and create an isolated environment:

```bash
git clone https://github.com/Ambetazam/Audio-Transcriber.git
cd Audio-Transcriber

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Verify the CLI:

```bash
audio-transcriber --help
audio-transcriber --version
```

## Basic usage

Transcribe one file:

```bash
audio-transcriber recording.m4a
```

By default this creates:

```text
transcripts/
└── recording.md
```

The Markdown file contains the detected language plus timestamped segments.

## Spanish recordings

You can explicitly tell the model that the audio is Spanish:

```bash
audio-transcriber recording.m4a --language es
```

For a folder containing several recordings:

```bash
audio-transcriber ./audio --language es
```

The tool searches recursively for supported formats.

## CPU workflow

The default profile is intentionally conservative:

```bash
audio-transcriber recording.m4a \
  --model small \
  --device cpu \
  --compute-type int8 \
  --language es
```

For a lighter/faster model on an older machine:

```bash
audio-transcriber recording.m4a --model base --language es
```

For higher accuracy, use a larger model when your hardware can handle it:

```bash
audio-transcriber recording.m4a --model large-v3 --language es
```

## NVIDIA GPU workflow

On a compatible CUDA setup, `faster-whisper` supports CUDA execution. For example:

```bash
audio-transcriber recording.m4a \
  --model large-v3 \
  --device cuda \
  --compute-type float16 \
  --language es
```

The upstream project documents additional GPU configurations and model options. 

## Evidence-friendly output

For academic or work evidence, keep timestamps enabled:

```bash
audio-transcriber conversation.m4a --language es --format md
```

Example output:

```markdown
# Transcription — conversation.m4a

## Metadata

- **Source:** `conversation.m4a`
- **Language:** `es`
- **Detection confidence:** `98.40%`

## Transcript

**[00:00:00.000 → 00:00:04.320]** Buenos días, ¿cómo vamos?

**[00:00:04.320 → 00:00:09.760]** Ya hice el cambio en el repositorio.
```

This is intentionally **not** presented as automatically verified evidence. Speech-to-text systems can mishear names, URLs, Git commands, accents, technical terms, or overlapping speech. Review the generated transcript against the original audio before submitting it.

## Useful options

```text
--model MODEL
--device {cpu,cuda,auto}
--compute-type TYPE
--language es
--task {transcribe,translate}
--format {txt,md}
--no-timestamps
--no-vad
--word-timestamps
--cpu-threads N
--output-dir PATH
```

See every option with:

```bash
audio-transcriber --help
```

## Suggested workflow for evidence

Keep your files outside Git:

```text
Evidence/
├── audio/
│   ├── whatsapp-01.m4a
│   ├── whatsapp-02.m4a
│   └── meeting-01.m4a
│
└── transcripts/
    ├── whatsapp-01.md
    ├── whatsapp-02.md
    └── meeting-01.md
```

Recommended process:

```text
Original audio
      ↓
Local transcription
      ↓
Human verification
      ↓
Corrected transcript
      ↓
Evidence report
```

Do not use the first machine-generated transcript as the final legal, academic, or administrative record without checking it.

## Development

Run tests with:

```bash
python -m pip install pytest
pytest
```

Run the package directly while developing:

```bash
python -m audio_transcriber.cli recording.m4a --language es
```

## Roadmap

- [x] Single-file transcription
- [x] Batch directory transcription
- [x] Language detection
- [x] Timestamped Markdown output
- [x] Plain-text output
- [x] CPU INT8 profile
- [ ] Optional speaker diarization
- [ ] Export to SRT/VTT
- [ ] JSON output with metadata
- [ ] Automatic transcript cleanup
- [ ] Configuration file
- [ ] Simple web interface
- [ ] Desktop GUI

## License

MIT.

## Author

**Jean Castaneda**

Systems Engineering Student • Software Engineer • Cybersecurity Researcher • AI Developer • Open Source Enthusiast
