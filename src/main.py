from audio.recorder import AudioRecorder
from audio.transcriber import AudioTranscriber
from commands.base import CommandProcessor

def main():
    # Configuration
    ACTIVATION_WORDS = ["furina", "purina"]
    
    # Initialize components
    recorder = AudioRecorder(duration=5)
    transcriber = AudioTranscriber()
    processor = CommandProcessor(ACTIVATION_WORDS)
    
    # No commands registered yet, just basic functionality
    print("=== Voice Assistant ===")
    print("Activation words:", ACTIVATION_WORDS)
    print("Press Enter to start recording...")
    
    while True:
        try:
            input()  # Wait for Enter
            
            # Record audio
            filename = recorder.record_audio()
            
            # Transcribe
            text = transcriber.transcribe_audio(filename)
            
            if text:
                # Process command
                result = processor.process_text(text)
                print(f"Result: {result}")
            else:
                print("Could not transcribe audio.")
                
        except KeyboardInterrupt:
            print("\nExiting assistant...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()