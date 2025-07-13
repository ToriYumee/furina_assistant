import sounddevice as sd
import soundfile as sf

class AudioRecorder:
    def __init__(self, duration=5, filename="recording.wav", samplerate=16000):
        self.duration = duration
        self.filename = filename
        self.samplerate = samplerate
    
    def record_audio(self):
        """Records audio for the specified duration"""
        print("Recording audio...")
        audio = sd.rec(
            int(self.duration * self.samplerate), 
            samplerate=self.samplerate, 
            channels=1, 
            dtype='int16'
        )
        sd.wait()
        sf.write(self.filename, audio, self.samplerate)
        print("Recording finished.")
        return self.filename