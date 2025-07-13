from datetime import datetime
from .base import BaseCommand

class TimeCommand(BaseCommand):
    """Command to get current time"""
    
    def __init__(self):
        keywords = ["hora", "time", "qué hora es", "what time"]
        description = "Gets the current time"
        super().__init__(keywords, description)
    
    def execute(self, command_text: str) -> str:
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        return f"Current time: {time_str}"

class DateCommand(BaseCommand):
    """Command to get current date"""
    
    def __init__(self):
        keywords = ["fecha", "date", "qué fecha", "what date", "hoy", "today"]
        description = "Gets the current date"
        super().__init__(keywords, description)
    
    def execute(self, command_text: str) -> str:
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        date_str_es = now.strftime("%A, %d de %B de %Y")
        return f"Today is: {date_str_es} ({date_str})"