---
title: Qwen3-ASR Demo
emoji: 🎙️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.33.0
app_file: app.py
pinned: false
license: apache-2.0
---

# Qwen3-ASR Demo

This Space demonstrates **Qwen3-ASR-1.7B**, a state-of-the-art automatic speech recognition model from the Qwen team, powered by **vLLM** for high-speed inference.

## Features

- **30+ Language Support**: Chinese, Cantonese, English, Japanese, Korean, Arabic, German, French, Spanish, Portuguese, and many more
- **Word/Character-level Timestamps**: Accurate timestamp alignment for each word (English) or character (Chinese)
- **Interactive Visualization**: Click on each word/character to hear the corresponding audio segment
- **vLLM Backend**: Fast inference speed for real-time transcription

## How to Use

1. Upload an audio file or record using your microphone
2. Select a language or leave "Auto" for automatic detection
3. Enable "Timestamps" for visualization (recommended)
4. Click "Transcribe" and see the results

## Models Used

- **ASR Model**: [Qwen/Qwen3-ASR-1.7B](https://huggingface.co/Qwen/Qwen3-ASR-1.7B)
- **Forced Aligner**: [Qwen/Qwen3-ForcedAligner-0.6B](https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B)

## Setup (For Space Owners)

This Space requires access to private models. You need to set up the `HF_TOKEN` secret:

1. Go to your Space Settings
2. Navigate to "Repository secrets"
3. Add a new secret with name `HF_TOKEN` and your Hugging Face access token as the value

## Links

- [GitHub Repository](https://github.com/Qwen/Qwen3-ASR)
- [Model Card](https://huggingface.co/Qwen/Qwen3-ASR-1.7B)

## License

Apache 2.0
