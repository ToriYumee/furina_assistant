from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class BaseCommand(ABC):
    """Base class for all commands"""
    
    def __init__(self, keywords: List[str], description: str):
        self.keywords = keywords
        self.description = description
    
    @abstractmethod
    def execute(self, command_text: str) -> str:
        """Executes the command and returns a response"""
        pass
    
    def can_execute(self, text: str) -> bool:
        """Checks if the command can be executed with the given text"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.keywords)
    
    def extract_parameters(self, text: str) -> str:
        """Extracts parameters from command by removing keywords"""
        text_lower = text.lower()
        for keyword in self.keywords:
            if keyword in text_lower:
                return text_lower.replace(keyword, "").strip()
        return text.strip()

class CommandProcessor:
    """Main command processor"""
    
    def __init__(self, activation_words: List[str]):
        self.activation_words = activation_words
        self.commands: List[BaseCommand] = []
    
    def register_command(self, command: BaseCommand):
        """Registers a new command"""
        self.commands.append(command)
    
    def process_text(self, text: str) -> Optional[str]:
        """Processes text and executes corresponding command"""
        if not self._is_valid_activation(text):
            return "No activation keyword found."
        
        # Remove activation word
        clean_command = self._clean_activation(text)
        
        # Find command that can execute
        for command in self.commands:
            if command.can_execute(clean_command):
                result = command.execute(clean_command)
                return result
        
        return f"Command not recognized: {clean_command}"
    
    def _is_valid_activation(self, text: str) -> bool:
        """Checks if text contains an activation word"""
        text_lower = text.lower()
        return any(word in text_lower for word in self.activation_words)
    
    def _clean_activation(self, text: str) -> str:
        """Removes activation words from text"""
        text_lower = text.lower()
        for word in self.activation_words:
            if word in text_lower:
                return text_lower.replace(word, "").strip()
        return text.strip()
    
    def list_commands(self) -> List[Dict[str, str]]:
        """Lists all registered commands"""
        return [
            {
                "keywords": command.keywords,
                "description": command.description
            }
            for command in self.commands
        ]