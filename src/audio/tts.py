import platform
import subprocess
import os
from abc import ABC, abstractmethod

class TTSEngine(ABC):
    """Abstract base class for Text-to-Speech engines"""
    
    @abstractmethod
    def speak(self, text: str) -> bool:
        """Speak the given text. Returns True if successful."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the TTS engine is available on this system"""
        pass

class WindowsTTS(TTSEngine):
    """Windows Text-to-Speech using built-in SAPI"""
    
    def speak(self, text: str) -> bool:
        try:
            # Using PowerShell with Windows Speech API
            command = f'powershell -Command "Add-Type -AssemblyName System.speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak(\'{text}\')"'
            subprocess.run(command, shell=True, check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
        except Exception:
            return False
    
    def is_available(self) -> bool:
        return platform.system() == "Windows"

class MacOSTTS(TTSEngine):
    """macOS Text-to-Speech using built-in 'say' command"""
    
    def speak(self, text: str) -> bool:
        try:
            subprocess.run(["say", text], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            return False
        except Exception:
            return False
    
    def is_available(self) -> bool:
        if platform.system() != "Darwin":
            return False
        try:
            subprocess.run(["which", "say"], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

class LinuxTTS(TTSEngine):
    """Linux Text-to-Speech using espeak or festival"""
    
    def __init__(self):
        self.engine = None
        if platform.system() == "Linux":
            self._detect_engine()
    
    def _detect_engine(self):
        """Detect available TTS engine on Linux"""
        engines = ["espeak", "festival", "spd-say"]
        for engine in engines:
            try:
                subprocess.run(["which", engine], check=True, capture_output=True)
                self.engine = engine
                break
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
    
    def speak(self, text: str) -> bool:
        if not self.engine:
            return False
        
        try:
            if self.engine == "espeak":
                subprocess.run(["espeak", text], check=True, capture_output=True)
            elif self.engine == "festival":
                subprocess.run(["festival", "--tts"], input=text, text=True, check=True, capture_output=True)
            elif self.engine == "spd-say":
                subprocess.run(["spd-say", text], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
        except Exception:
            return False
    
    def is_available(self) -> bool:
        return platform.system() == "Linux" and self.engine is not None

class PyttsxTTS(TTSEngine):
    """Cross-platform TTS using pyttsx3 library"""
    
    def __init__(self):
        self.engine = None
        self._init_engine()
    
    def _init_engine(self):
        """Initialize pyttsx3 engine"""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            # Configure voice properties
            self.engine.setProperty('rate', 150)  # Speed
            self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        except ImportError:
            print("pyttsx3 not installed. Install with: pip install pyttsx3")
            self.engine = None
        except Exception as e:
            print(f"Error initializing pyttsx3: {e}")
            self.engine = None
    
    def speak(self, text: str) -> bool:
        if not self.engine:
            return False
        
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            print(f"Error speaking with pyttsx3: {e}")
            return False
    
    def is_available(self) -> bool:
        return self.engine is not None

class TextToSpeech:
    """Main TTS class that automatically selects the best available engine"""
    
    def __init__(self, prefer_pyttsx=False):
        self.engines = []
        self.current_engine = None
        self.enabled = True
        
        print("Initializing TTS engines...")
        
        # Initialize engines in order of preference based on OS
        current_os = platform.system()
        
        if current_os == "Windows":
            self.engines = [WindowsTTS(), PyttsxTTS()]
        elif current_os == "Darwin":  # macOS
            self.engines = [MacOSTTS(), PyttsxTTS()]
        elif current_os == "Linux":
            self.engines = [LinuxTTS(), PyttsxTTS()]
        else:
            # Unknown OS, try pyttsx3 only
            self.engines = [PyttsxTTS()]
        
        # If user prefers pyttsx3, put it first
        if prefer_pyttsx and len(self.engines) > 1:
            pyttsx_engine = next((e for e in self.engines if isinstance(e, PyttsxTTS)), None)
            if pyttsx_engine:
                self.engines.remove(pyttsx_engine)
                self.engines.insert(0, pyttsx_engine)
        
        # Select first available engine
        for engine in self.engines:
            print(f"Testing {engine.__class__.__name__}...")
            if engine.is_available():
                self.current_engine = engine
                print(f"✓ TTS Engine selected: {engine.__class__.__name__}")
                break
            else:
                print(f"✗ {engine.__class__.__name__} not available")
        
        if not self.current_engine:
            print("⚠️  No TTS engine available")
            self.enabled = False
    
    def speak(self, text: str) -> bool:
        """Speak the given text using the selected engine"""
        if not self.enabled or not self.current_engine:
            print(f"TTS disabled. Text: {text}")
            return False
        
        if not text or not text.strip():
            return False
        
        # Try to speak with current engine
        success = self.current_engine.speak(text)
        
        # If it fails, try other available engines
        if not success:
            print(f"Primary TTS engine failed, trying alternatives...")
            for engine in self.engines:
                if engine != self.current_engine and engine.is_available():
                    print(f"Trying {engine.__class__.__name__}...")
                    if engine.speak(text):
                        print(f"Switched to {engine.__class__.__name__}")
                        self.current_engine = engine
                        return True
            print("All TTS engines failed")
            return False
        
        return success
    
    def toggle(self) -> bool:
        """Toggle TTS on/off. Returns new state."""
        self.enabled = not self.enabled
        return self.enabled
    
    def is_enabled(self) -> bool:
        """Check if TTS is enabled and available"""
        return self.enabled and self.current_engine is not None
    
    def get_engine_info(self) -> str:
        """Get information about the current TTS engine"""
        if not self.current_engine:
            return "No TTS engine available"
        return f"Engine: {self.current_engine.__class__.__name__}, Enabled: {self.enabled}"