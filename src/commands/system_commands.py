import subprocess
import platform
from .base import BaseCommand

class SystemCommand(BaseCommand):
    """Command for system operations"""
    
    def __init__(self):
        keywords = ["apaga", "apagar", "shutdown", "reinicia", "reiniciar", "restart", "suspender", "sleep"]
        description = "System operations (shutdown, restart, sleep)"
        super().__init__(keywords, description)
    
    def execute(self, command_text: str) -> str:
        os_name = platform.system()
        command_lower = command_text.lower()
        
        # Safety confirmation for destructive operations
        if any(word in command_lower for word in ["apaga", "apagar", "shutdown", "reinicia", "reiniciar", "restart"]):
            return "System operations disabled for safety. Enable in system_commands.py if needed."
        
        # Safe operations
        if any(word in command_lower for word in ["suspender", "sleep"]):
            try:
                if os_name == "Windows":
                    subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=True)
                elif os_name == "Darwin":  # macOS
                    subprocess.run(["pmset", "sleepnow"], check=True)
                elif os_name == "Linux":
                    subprocess.run(["systemctl", "suspend"], check=True)
                return "Putting system to sleep..."
            except subprocess.CalledProcessError as e:
                return f"Error executing sleep command: {e}"
            except Exception as e:
                return f"Unexpected error: {e}"
        
        return "System command not recognized or not available."

class VolumeCommand(BaseCommand):
    """Command to control system volume"""
    
    def __init__(self):
        keywords = ["volumen", "volume", "subir volumen", "bajar volumen", "silencio", "mute"]
        description = "Controls system volume"
        super().__init__(keywords, description)
    
    def execute(self, command_text: str) -> str:
        os_name = platform.system()
        command_lower = command_text.lower()
        
        try:
            if "subir" in command_lower or "up" in command_lower:
                if os_name == "Windows":
                    # Windows volume control would need additional libraries
                    return "Volume control not implemented for Windows yet"
                elif os_name == "Darwin":  # macOS
                    subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"], check=True)
                    return "Volume increased"
                elif os_name == "Linux":
                    subprocess.run(["amixer", "set", "Master", "10%+"], check=True)
                    return "Volume increased"
            
            elif "bajar" in command_lower or "down" in command_lower:
                if os_name == "Windows":
                    return "Volume control not implemented for Windows yet"
                elif os_name == "Darwin":  # macOS
                    subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"], check=True)
                    return "Volume decreased"
                elif os_name == "Linux":
                    subprocess.run(["amixer", "set", "Master", "10%-"], check=True)
                    return "Volume decreased"
            
            elif "silencio" in command_lower or "mute" in command_lower:
                if os_name == "Windows":
                    return "Mute control not implemented for Windows yet"
                elif os_name == "Darwin":  # macOS
                    subprocess.run(["osascript", "-e", "set volume with output muted"], check=True)
                    return "Audio muted"
                elif os_name == "Linux":
                    subprocess.run(["amixer", "set", "Master", "toggle"], check=True)
                    return "Audio toggled"
            
            return "Volume command not recognized"
            
        except subprocess.CalledProcessError as e:
            return f"Error controlling volume: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"