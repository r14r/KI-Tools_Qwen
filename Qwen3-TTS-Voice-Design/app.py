import base64
import json
import gradio as gr
import numpy as np
import requests
import os
import io
import soundfile as sf

# Ensure API_KEY is set in your environment variables
API_KEY = os.environ.get('API_KEY', 'your_api_key_here')

def voice_design(prompt, text):
    url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "model": "qwen-voice-design",
        "input": {
            "action": "create",
            "voice_prompt": prompt,
            "preview_text": text,
            "target_model": "qwen3-tts-vd-realtime-2025-12-16",
            "preferred_name": "default"
        },
        "parameters": {
            "sample_rate": 24000,
            "response_format": "wav"
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    sr = 24000

    if response.status_code == 200:
        res_json = json.loads(response.text)
        if 'output' in res_json and 'preview_audio' in res_json['output']:
            base64_audio = res_json['output']['preview_audio']['data']
            audio_bytes = base64.b64decode(base64_audio)

            audio_buffer = io.BytesIO(audio_bytes)
            audio_np, sr = sf.read(audio_buffer)
            return (sr, audio_np)
        else:
            print("Error in response output:", res_json)
            return (sr, np.array([]))
    else:
        print(f"API Error: {response.status_code} - {response.text}")
        return (sr, np.array([]))

def tts_interface(text: str, instruct: str):
    return voice_design(instruct, text)

def _launch_demo():
    # English Example Data
    examples = [
        [
            "Welcome to the speech synthesis system. Please enter the text you would like to have read aloud.",
            "A clear and natural female voice, moderate speed, stable tone, suitable for news broadcasting or daily conversation."
        ],
        [
            "He's not going to make it... it's all my fault. He only trusts you, Professor Ye. Please, you have to save him!",
            "Standard pronunciation with a dramatic, sobbing quality. The voice is slightly raspy and tense, conveying deep sorrow and desperate pleading."
        ],
        [
            "Our entire fleet and army are overdue for an equipment upgrade. It is time to modernize.",
            "A loud, powerful male voice exhibiting resilience and authority. The pace is brisk and fluent, slowing down slightly at the end for emphasis and decisiveness."
        ],
        [
            "Becoming a scientist is the dream of countless children. We must make scientific work attractive and a profession that children aspire to. We want to give their dreams the wings of technology.",
            "Professional broadcasting style. The pace starts slow and accelerates, with a bright, solid timbre. The tone should be inspiring, passionate, and persuasive."
        ],
        [
            "I have a couple of rifles here, but we have never had the habit of surrendering our weapons.",
            "A calm and confident tone. The speed is steady, with very clear articulation. The voice should feel firm and certain, with a slight downward inflection at the end."
        ],
        [
            "They say a family stays together through the wind and rain. I've spent my life on the waves just for a net of fish, but I never imagined a storm could be for the people. Isn't this a great opportunity?",
            "A young female voice, brave and determined, filled with idealism and warmth. High-mid pitch range, distinct cadence, and transitioning from steady to passionate."
        ],
        [
            "In this village, there is a very traditional and unique delicacy called the Green Leaf Feast. I bet I'll get to taste it today! Look, those two girls are gathering leaves right now. Let’s go ask them about it.",
            "Cheerful and extroverted personality. Fast but fluent pace, with the pitch rising at key moments to emphasize excitement and curiosity about the food."
        ],
        [
            "I have a big brother named Wang. He’s got a huge appetite for soup! Even without a weapon in his hand, his words fire faster than a machine gun.",
            "A bright, high-pitched young girl's voice. Lively and animated tone that engages the listener, with a loud and clear volume reflecting an active personality."
        ]
    ]
    
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            # 🎙️ Qwen3-TTS Voice Design Demo
            
            Effortlessly design custom voice profiles using natural language descriptions.
            
            **How to use:**
            1. Enter the content in the **Input Text** box.
            2. Describe the desired voice (gender, age, speed, emotion) in the **Voice Instruction** box.
            3. Click **Generate Voice** or try one of the **Quick Examples** below.
            """
        )
        
        with gr.Row(equal_height=True):
            with gr.Column(scale=3):
                text_input = gr.Textbox(
                    label="📝 Input Text",
                    placeholder="Enter the text you want to synthesize...",
                    value="Welcome to the speech synthesis system. Please enter the text you would like to have read aloud.",
                    lines=6,
                )
                instruct_input = gr.Textbox(
                    label="🎨 Voice Instruction",
                    placeholder="Describe the voice: gender, age, speed, tone, emotion, scenario...",
                    value="A clear and natural female voice, moderate speed, stable tone, suitable for news broadcasting or daily conversation.",
                    lines=6,
                )
                
                with gr.Row():
                    clear_btn = gr.Button("🗑️ Clear", variant="secondary", scale=1)
                    generate_btn = gr.Button("🎵 Generate Voice", variant="primary", scale=3, size="lg")
            
            with gr.Column(scale=3):
                result_output = gr.Audio(
                    label="🔊 Generated Result",
                    type="numpy"
                )
                
                gr.Markdown(
                    """
                    ### 💡 Voice Prompting Tips
                    
                    Try describing these dimensions:
                    - **Persona**: Male/Female, Young/Middle-aged/Elderly.
                    - **Pace**: Fast, moderate, or slow.
                    - **Timbre**: Clear, deep, sweet, magnetic, or raspy.
                    - **Emotion**: Calm, enthusiastic, gentle, serious, or lively.
                    - **Scenario**: News, storytelling, sales, or classroom.
                    """
                )
        
        # Examples Section
        gr.Markdown("### 📚 Quick Examples")
        gr.Examples(
            examples=examples,
            inputs=[text_input, instruct_input],
            outputs=result_output,
            fn=tts_interface,
            cache_examples=False,
            label="Click an example to try it out"
        )
        
        # Event Bindings
        generate_btn.click(
            fn=tts_interface,
            inputs=[text_input, instruct_input],
            outputs=[result_output]
        )
        
        clear_btn.click(
            fn=lambda: ("", "", None),
            inputs=[],
            outputs=[text_input, instruct_input, result_output]
        )
        
        gr.Markdown(
            """
            ---
            **Note:** Generation time depends on text length and server response. Please wait a moment after clicking generate.
            """
        )
    
    # Launch Settings
    demo.queue(default_concurrency_limit=100, max_size=20).launch(
        max_threads=100,
        share=False
    )

if __name__ == "__main__":
    _launch_demo()