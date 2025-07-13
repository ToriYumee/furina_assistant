import subprocess
import platform
from .base import BaseCommand

class AppLauncherCommand(BaseCommand):
    """Command to launch applications"""
    
    def __init__(self):
        keywords = ["abre", "abrir", "open", "launch", "ejecuta", "execute"]
        description = "Opens applications (browser, calculator, notepad, etc.)"
        super().__init__(keywords, description)
        
        # Application mappings for different OS
        self.apps = {
            "Windows": {
                "navegador": "start chrome",
                "browser": "start chrome",
                "calculadora": "calc",
                "calculator": "calc",
                "notepad": "notepad",
                "bloc de notas": "notepad",
                "explorador": "explorer",
                "explorer": "explorer",
                "paint": "mspaint",
                "cmd": "cmd",
                "terminal": "cmd"
            },
            "Darwin": {  # macOS
                "navegador": "open -a Safari",
                "browser": "open -a Safari",
                "calculadora": "open -a Calculator",
                "calculator": "open -a Calculator",
                "notepad": "open -a TextEdit",
                "bloc de notas": "open -a TextEdit",
                "explorador": "open .",
                "explorer": "open .",
                "terminal": "open -a Terminal"
            },
            "Linux": {
                "navegador": "firefox",
                "browser": "firefox",
                "calculadora": "gnome-calculator",
                "calculator": "gnome-calculator",
                "notepad": "gedit",
                "bloc de notas": "gedit",
                "explorador": "nautilus",
                "explorer": "nautilus",
                "terminal": "gnome-terminal"
            }
        }
    
    def execute(self, command_text: str) -> str:
        os_name = platform.system()
        apps_for_os = self.apps.get(os_name, {})
        
        # Extract app name from command
        app_name = self.extract_parameters(command_text).lower()
        
        if not app_name:
            available_apps = ", ".join(apps_for_os.keys())
            return f"Please specify an application. Available: {available_apps}"
        
        # Find matching app
        command_to_run = None
        for app_key, app_command in apps_for_os.items():
            if app_key in app_name:
                command_to_run = app_command
                break
        
        if not command_to_run:
            available_apps = ", ".join(apps_for_os.keys())
            return f"Application '{app_name}' not found. Available: {available_apps}"
        
        try:
            if os_name == "Windows":
                subprocess.run(command_to_run, shell=True, check=True)
            else:
                subprocess.run(command_to_run.split(), check=True)
            return f"Opening {app_name}..."
        except subprocess.CalledProcessError as e:
            return f"Error opening {app_name}: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"