from audio.recorder import AudioRecorder
from audio.transcriber import AudioTranscriber
from audio.tts import TextToSpeech
from commands.base import CommandProcessor
from commands.time_commands import TimeCommand, DateCommand
from commands.app_commands import AppLauncherCommand
from commands.system_commands import SystemCommand, VolumeCommand
from commands.help_commands import HelpCommand, GreetingCommand
from commands.tts_commands import TTSControlCommand, RepeatCommand

def main():
    # Configuration
    ACTIVATION_WORDS = ["furina", "purina"]
    
    # Initialize components
    recorder = AudioRecorder(duration=5)
    transcriber = AudioTranscriber()
    tts = TextToSpeech(prefer_pyttsx=False)  # Use system TTS first
    processor = CommandProcessor(ACTIVATION_WORDS)
    
    # Register basic commands
    processor.register_command(TimeCommand())
    processor.register_command(DateCommand())
    processor.register_command(AppLauncherCommand())
    processor.register_command(SystemCommand())
    processor.register_command(VolumeCommand())
    processor.register_command(GreetingCommand())
    
    # TTS-related commands
    tts_control = TTSControlCommand()
    tts_control.set_tts_engine(tts)
    processor.register_command(tts_control)
    
    repeat_cmd = RepeatCommand()
    repeat_cmd.set_tts_engine(tts)
    processor.register_command(repeat_cmd)
    
    # Help command needs processor reference
    help_cmd = HelpCommand()
    help_cmd.set_processor(processor)
    processor.register_command(help_cmd)
    
    print("=== Voice Assistant with TTS ===")
    print("Activation words:", ACTIVATION_WORDS)
    print(f"Commands loaded: {len(processor.commands)}")
    print(f"TTS Status: {tts.get_engine_info()}")
    print("Say 'Furina ayuda' for available commands")
    print("Press Enter to start recording...")
    
    last_response = ""
    
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
                
                # Store last response for repeat command
                last_response = result
                repeat_cmd.set_last_response(last_response)
                
                # Speak the result if TTS is enabled
                if tts.is_enabled():
                    # Clean up the text for better speech
                    speech_text = result
                    if speech_text.startswith("Result: "):
                        speech_text = speech_text[8:]  # Remove "Result: " prefix
                    
                    tts.speak(speech_text)
                
            else:
                error_msg = "Could not transcribe audio."
                print(error_msg)
                if tts.is_enabled():
                    tts.speak("Sorry, I couldn't understand that.")
                
        except KeyboardInterrupt:
            print("\nExiting assistant...")
            if tts.is_enabled():
                tts.speak("Goodbye!")
            break
        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            if tts.is_enabled():
                tts.speak("An error occurred.")

if __name__ == "__main__":
    main()