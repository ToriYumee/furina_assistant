from audio.recorder import AudioRecorder
from audio.transcriber import AudioTranscriber
from commands.base import CommandProcessor
from commands.time_commands import TimeCommand, DateCommand
from commands.app_commands import AppLauncherCommand
from commands.system_commands import SystemCommand, VolumeCommand
from commands.help_commands import HelpCommand, GreetingCommand

def main():
    # Configuration
    ACTIVATION_WORDS = ["furina", "purina"]
    
    # Initialize components
    recorder = AudioRecorder(duration=5)
    transcriber = AudioTranscriber()
    processor = CommandProcessor(ACTIVATION_WORDS)
    
    # Register commands
    processor.register_command(TimeCommand())
    processor.register_command(DateCommand())
    processor.register_command(AppLauncherCommand())
    processor.register_command(SystemCommand())
    processor.register_command(VolumeCommand())
    processor.register_command(GreetingCommand())
    
    # Help command needs processor reference
    help_cmd = HelpCommand()
    help_cmd.set_processor(processor)
    processor.register_command(help_cmd)
    
    print("=== Voice Assistant ===")
    print("Activation words:", ACTIVATION_WORDS)
    print(f"Commands loaded: {len(processor.commands)}")
    print("Say 'Furina ayuda' for available commands")
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