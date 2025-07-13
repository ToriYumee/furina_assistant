from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class AudioTranscriber:
    def __init__(self):
        self.client = OpenAI()
    
    def transcribe_audio(self, filename):
        """Transcribes audio file using Whisper"""
        try:
            with open(filename, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="es"
                )
            text = transcript.text
            print("Transcribed text:", text)
            return text
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None