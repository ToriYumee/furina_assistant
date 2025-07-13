from .base import BaseCommand

class TTSControlCommand(BaseCommand):
    """Command to control Text-to-Speech settings"""
    
    def __init__(self, tts_engine=None):
        keywords = ["voz", "voice", "hablar", "speak", "silenciar voz", "mute voice", "activar voz", "enable voice"]
        description = "Controls text-to-speech voice output"
        super().__init__(keywords, description)
        self.tts_engine = tts_engine
    
    def set_tts_engine(self, tts_engine):
        """Set the TTS engine reference"""
        self.tts_engine = tts_engine
    
    def execute(self, command_text: str) -> str:
        if not self.tts_engine:
            return "TTS engine not available"
        
        command_lower = command_text.lower()
        
        if any(word in command_lower for word in ["silenciar", "mute", "desactivar", "disable"]):
            if self.tts_engine.enabled:
                self.tts_engine.toggle()
                return "Voice output disabled"
            else:
                return "Voice output is already disabled"
        
        elif any(word in command_lower for word in ["activar", "enable", "encender", "turn on"]):
            if not self.tts_engine.enabled:
                self.tts_engine.toggle()
                return "Voice output enabled"
            else:
                return "Voice output is already enabled"
        
        elif any(word in command_lower for word in ["estado", "status", "info"]):
            return self.tts_engine.get_engine_info()
        
        elif any(word in command_lower for word in ["prueba", "test"]):
            success = self.tts_engine.speak("This is a voice test. TTS is working correctly.")
            if success:
                return "Voice test completed"
            else:
                return "Voice test failed"
        
        return "Voice command not recognized. Try: 'activar voz', 'silenciar voz', 'estado voz', or 'prueba voz'"

class RepeatCommand(BaseCommand):
    """Command to repeat the last response"""
    
    def __init__(self, tts_engine=None):
        keywords = ["repite", "repeat", "di otra vez", "say again"]
        description = "Repeats the last response"
        super().__init__(keywords, description)
        self.tts_engine = tts_engine
        self.last_response = ""
    
    def set_tts_engine(self, tts_engine):
        """Set the TTS engine reference"""
        self.tts_engine = tts_engine
    
    def set_last_response(self, response: str):
        """Set the last response to be repeated"""
        self.last_response = response
    
    def execute(self, command_text: str) -> str:
        if not self.last_response:
            return "No previous response to repeat"
        
        if self.tts_engine and self.tts_engine.is_enabled():
            self.tts_engine.speak(self.last_response)
        
        return f"Repeating: {self.last_response}"