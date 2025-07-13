import os
import sounddevice as sd
import soundfile as sf
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

DURACION = 5  # segundos
FILENAME = "grabacion.wav"
SAMPLERATE = 16000

def grabar_audio():
    print("Grabando audio...")
    audio = sd.rec(int(DURACION * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='int16')
    sd.wait()
    sf.write(FILENAME, audio, SAMPLERATE)
    print("Grabación finalizada.")

def transcribir_audio():
    audio_file = open(FILENAME, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="es"
    )
    texto = transcript.text
    print("Texto transcrito:", texto)
    return texto

def main():
    grabar_audio()
    texto = transcribir_audio()
    
    palabras_clave = ["furina", "purina"]
    
    comando_detectado = False
    for palabra in palabras_clave:
        if palabra in texto.lower():
            comando = texto.lower().replace(palabra, "").strip()
            print(f"Comando detectado: {comando}")
            comando_detectado = True
            break
    
    if not comando_detectado:
        print("No se encontró ninguna palabra clave de activación.")

if __name__ == "__main__":
    main()