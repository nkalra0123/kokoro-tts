import gradio as gr
from kokoro_onnx import Kokoro
import soundfile as sf
import tempfile
import os

class TextToSpeechApp:
    def __init__(self):
        # Initialize Kokoro
        self.kokoro = Kokoro("kokoro-v0_19.onnx", "voices.json")
        
        # Available voices
        self.voices = [
            'af', 'af_bella', 'af_nicole', 'af_sarah', 'af_sky',
            'am_adam', 'am_michael', 'bf_emma', 'bf_isabella',
            'bm_george', 'bm_lewis'
        ]

    def generate_speech(self, text, voice, speed):
        try:
            # Generate audio
            samples, sample_rate = self.kokoro.create(
                text,
                voice=voice,
                speed=float(speed)
            )
            
            # Create temporary file
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, "output.wav")
            
            # Save to temporary file
            sf.write(temp_path, samples, sample_rate)
            
            return temp_path
            
        except Exception as e:
            return f"Error: {str(e)}"

    def create_interface(self):
        interface = gr.Interface(
            fn=self.generate_speech,
            inputs=[
                gr.Textbox(label="Enter text to convert", lines=5),
                gr.Dropdown(choices=self.voices, label="Select Voice", value=self.voices[0]),
                gr.Slider(minimum=0.5, maximum=2.0, value=1.0, step=0.1, label="Speech Speed")
            ],
            outputs=gr.Audio(label="Generated Speech"),
            title="Text to Speech Converter",
            description="Convert text to speech using different voices and speeds."
        )
        return interface

def main():
    app = TextToSpeechApp()
    interface = app.create_interface()
    # Launch with a public URL
    interface.launch(server_name="0.0.0.0", share=True)

if __name__ == "__main__":
    main()