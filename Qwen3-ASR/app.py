# coding=utf-8
# Copyright 2026 The Alibaba Qwen team.
# SPDX-License-Identifier: Apache-2.0
"""
Qwen3-ASR Demo for Huggingface Spaces with ZeroGPU support.
Showcases the 1.7B model with timestamp visualization.
"""

import base64
import io
import os
from typing import Any, Dict, List, Optional, Tuple, Union

import gradio as gr
import numpy as np
import spaces
import torch
from huggingface_hub import login
from scipy.io.wavfile import write as wav_write

# Login to Hugging Face with token from environment variable
HF_TOKEN = os.environ.get("HF_TOKEN")
if HF_TOKEN:
    login(token=HF_TOKEN)

def _title_case_display(s: str) -> str:
    s = (s or "").strip()
    s = s.replace("_", " ")
    return " ".join([w[:1].upper() + w[1:] if w else "" for w in s.split()])


def _build_choices_and_map(items: Optional[List[str]]) -> Tuple[List[str], Dict[str, str]]:
    if not items:
        return [], {}
    display = [_title_case_display(x) for x in items]
    mapping = {d: r for d, r in zip(display, items)}
    return display, mapping


def _normalize_audio(wav, eps=1e-12, clip=True):
    x = np.asarray(wav)

    if np.issubdtype(x.dtype, np.integer):
        info = np.iinfo(x.dtype)
        if info.min < 0:
            y = x.astype(np.float32) / max(abs(info.min), info.max)
        else:
            mid = (info.max + 1) / 2.0
            y = (x.astype(np.float32) - mid) / mid
    elif np.issubdtype(x.dtype, np.floating):
        y = x.astype(np.float32)
        m = np.max(np.abs(y)) if y.size else 0.0
        if m > 1.0 + 1e-6:
            y = y / (m + eps)
    else:
        raise TypeError(f"Unsupported dtype: {x.dtype}")

    if clip:
        y = np.clip(y, -1.0, 1.0)

    if y.ndim > 1:
        y = np.mean(y, axis=-1).astype(np.float32)

    return y


def _audio_to_tuple(audio: Any) -> Optional[Tuple[np.ndarray, int]]:
    """
    Accept gradio audio:
      - {"sampling_rate": int, "data": np.ndarray}
      - (sr, np.ndarray)  [some gradio versions]
    Return: (wav_float32_mono, sr)
    """
    if audio is None:
        return None

    if isinstance(audio, dict) and "sampling_rate" in audio and "data" in audio:
        sr = int(audio["sampling_rate"])
        wav = _normalize_audio(audio["data"])
        return wav, sr

    if isinstance(audio, tuple) and len(audio) == 2:
        a0, a1 = audio
        if isinstance(a0, int):
            sr = int(a0)
            wav = _normalize_audio(a1)
            return wav, sr
        if isinstance(a1, int):
            wav = _normalize_audio(a0)
            sr = int(a1)
            return wav, sr

    return None


def _parse_audio_any(audio: Any) -> Union[str, Tuple[np.ndarray, int]]:
    if audio is None:
        raise ValueError("Audio is required.")
    at = _audio_to_tuple(audio)
    if at is not None:
        return at
    raise ValueError("Unsupported audio input format.")


def _make_timestamp_html(audio_upload: Any, timestamps: Any) -> str:
    """
    Build HTML with per-token audio slices, using base64 data URLs.
    """
    at = _audio_to_tuple(audio_upload)
    if at is None:
        return "<div style='color:#666'>No audio available for visualization.</div>"
    audio, sr = at

    if not timestamps:
        return "<div style='color:#666'>No timestamps to visualize.</div>"
    if not isinstance(timestamps, list):
        return "<div style='color:#666'>Invalid timestamp format.</div>"

    html_content = """
    <style>
        .word-alignment-container { display: flex; flex-wrap: wrap; gap: 10px; }
        .word-box {
            border: 1px solid #ddd; border-radius: 8px; padding: 10px;
            background-color: #f9f9f9; box-shadow: 0 2px 4px rgba(0,0,0,0.06);
            text-align: center;
        }
        .word-text { font-size: 18px; font-weight: 700; margin-bottom: 5px; }
        .word-time { font-size: 12px; color: #666; margin-bottom: 8px; }
        .word-audio audio { width: 140px; height: 30px; }
        details { border: 1px solid #ddd; border-radius: 6px; padding: 10px; background-color: #f7f7f7; }
        summary { font-weight: 700; cursor: pointer; }
    </style>
    """

    html_content += """
    <details open>
        <summary>Timestamps Visualization (click each word to hear the audio segment)</summary>
        <div class="word-alignment-container" style="margin-top: 14px;">
    """

    for item in timestamps:
        if not isinstance(item, dict):
            continue
        word = str(item.get("text", "") or "")
        start = item.get("start_time", None)
        end = item.get("end_time", None)
        if start is None or end is None:
            continue

        start = float(start)
        end = float(end)
        if end <= start:
            continue

        start_sample = max(0, int(start * sr))
        end_sample = min(len(audio), int(end * sr))
        if end_sample <= start_sample:
            continue

        seg = audio[start_sample:end_sample]
        seg_i16 = (np.clip(seg, -1.0, 1.0) * 32767.0).astype(np.int16)

        mem = io.BytesIO()
        wav_write(mem, sr, seg_i16)
        mem.seek(0)
        b64 = base64.b64encode(mem.read()).decode("utf-8")
        audio_src = f"data:audio/wav;base64,{b64}"

        html_content += f"""
        <div class="word-box">
            <div class="word-text">{word}</div>
            <div class="word-time">{start:.3f}s - {end:.3f}s</div>
            <div class="word-audio">
                <audio controls preload="none" src="{audio_src}"></audio>
            </div>
        </div>
        """

    html_content += "</div></details>"
    return html_content



from qwen_asr import Qwen3ASRModel

asr = Qwen3ASRModel.from_pretrained(
    "Qwen/Qwen3-ASR-1.7B",
    dtype=torch.bfloat16,
    device_map="cuda",
    forced_aligner="Qwen/Qwen3-ForcedAligner-0.6B",
    forced_aligner_kwargs=dict(
        dtype=torch.bfloat16,
        device_map="cuda",
    ),
    max_inference_batch_size=16,
    attn_implementation="kernels-community/flash-attn3",
)


# Supported languages
SUPPORTED_LANGUAGES = [
    "Chinese", "Cantonese", "English", "Arabic", "German", "French",
    "Spanish", "Portuguese", "Indonesian", "Italian", "Korean", "Russian",
    "Thai", "Vietnamese", "Japanese", "Turkish", "Hindi", "Malay",
    "Dutch", "Swedish", "Danish", "Finnish", "Polish", "Czech",
    "Filipino", "Persian", "Greek", "Romanian", "Hungarian", "Macedonian"
]

lang_choices_disp, lang_map = _build_choices_and_map(SUPPORTED_LANGUAGES)
lang_choices = ["Auto"] + lang_choices_disp


@spaces.GPU
def transcribe(audio_upload: Any, lang_disp: str, return_ts: bool, progress=gr.Progress(track_tqdm=True)):
    """
    Main transcription function with ZeroGPU support.
    """
    if audio_upload is None:
        return "", "", None, "<div style='color:#666'>Please upload an audio file first.</div>"

    try:
        audio_obj = _parse_audio_any(audio_upload)
    except ValueError as e:
        return "", "", None, f"<div style='color:red'>Error: {str(e)}</div>"

    language = None
    if lang_disp and lang_disp != "Auto":
        language = lang_map.get(lang_disp, lang_disp)

    # Perform transcription
    results = asr.transcribe(
        audio=audio_obj,
        language=language,
        return_time_stamps=return_ts,
    )

    if not isinstance(results, list) or len(results) != 1:
        return "", "", None, "<div style='color:red'>Unexpected result format.</div>"

    r = results[0]

    # Extract timestamps
    ts_payload = None
    if return_ts and hasattr(r, "time_stamps") and r.time_stamps:
        ts_payload = [
            dict(
                text=getattr(t, "text", ""),
                start_time=getattr(t, "start_time", 0),
                end_time=getattr(t, "end_time", 0),
            )
            for t in r.time_stamps
        ]

    # Note: Visualization is generated separately when user clicks "Visualize Timestamps"
    return (
        getattr(r, "language", "") or "",
        getattr(r, "text", "") or "",
        ts_payload,
        "",  # Empty HTML - visualization is triggered by separate button
    )


def visualize_timestamps(audio_upload: Any, timestamps_json: Any):
    """Generate timestamp visualization from existing results."""
    if timestamps_json is None:
        return "<div style='color:#666'>No timestamps available. Please run transcription with timestamps enabled first.</div>"
    return _make_timestamp_html(audio_upload, timestamps_json)


# Build Gradio interface
theme = gr.themes.Soft(
    font=[gr.themes.GoogleFont("Source Sans Pro"), "Arial", "sans-serif"],
)

css = """
.gradio-container {max-width: none !important;}
.main-title {text-align: center; margin-bottom: 20px;}
"""

with gr.Blocks(theme=theme, css=css, title="Qwen3-ASR Demo") as demo:
    gr.Markdown(
        """
# Qwen3-ASR Demo

**Model:** `Qwen3-ASR-1.7B` with `Qwen3-ForcedAligner-0.6B`

Qwen3-ASR is a state-of-the-art automatic speech recognition model that supports **52+ languages and dialect** with high accuracy.
This demo showcases the 1.7B model which provides excellent multilingual recognition capabilities.

**Features:**
- Multi-language ASR (Chinese, English, Japanese, Korean, and 52+ more languages and dialect)
- Word/character-level timestamp alignment
- Interactive timestamp visualization - hear each word/character segment!
"""
    )

    with gr.Row():
        with gr.Column(scale=2):
            audio_in = gr.Audio(
                label="Upload Audio",
                type="numpy",
                sources=["upload", "microphone"],
            )
            lang_in = gr.Dropdown(
                label="Language (leave 'Auto' for automatic detection)",
                choices=lang_choices,
                value="Auto",
                interactive=True,
            )
            ts_in = gr.Checkbox(
                label="Enable Timestamps (recommended for visualization)",
                value=True,
            )
            btn = gr.Button("Transcribe", variant="primary", size="lg")

        with gr.Column(scale=2):
            out_lang = gr.Textbox(label="Detected Language", lines=1, interactive=False)
            out_text = gr.Textbox(label="Transcription Result", lines=10, interactive=False)

        with gr.Column(scale=3):
            out_ts = gr.JSON(label="Timestamps (JSON)")
            viz_btn = gr.Button("Visualize Timestamps", variant="secondary")

    with gr.Row():
        out_ts_html = gr.HTML(label="Timestamps Visualization")

    # Event handlers
    btn.click(
        transcribe,
        inputs=[audio_in, lang_in, ts_in],
        outputs=[out_lang, out_text, out_ts, out_ts_html],
    )
    viz_btn.click(
        visualize_timestamps,
        inputs=[audio_in, out_ts],
        outputs=[out_ts_html],
    )

    gr.Markdown(
        """
---
**Links:** [Qwen3-ASR on Hugging Face](https://huggingface.co/collections/Qwen/qwen3-asr) | [GitHub Repository](https://github.com/QwenLM/Qwen3-ASR)
"""
    )


if __name__ == "__main__":
    demo.launch()