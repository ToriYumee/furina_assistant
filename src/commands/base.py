from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple
from utils.fuzzy_matcher import SmartCommandMatcher

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
    """Main command processor with enhanced fuzzy matching"""
    
    def __init__(self, activation_words: List[str], fuzzy_threshold: float = 60.0):
        self.activation_words = activation_words
        self.commands: List[BaseCommand] = []
        self.fuzzy_matcher = SmartCommandMatcher(threshold=fuzzy_threshold)
        self.stats = {
            'total_commands': 0,
            'fuzzy_matches': 0,
            'exact_matches': 0,
            'failed_matches': 0
        }
    
    def register_command(self, command: BaseCommand):
        """Registers a new command"""
        self.commands.append(command)
    
    def process_text(self, text: str) -> Optional[str]:
        """Processes text and executes corresponding command with fuzzy matching"""
        self.stats['total_commands'] += 1
        
        if not self._is_valid_activation(text):
            return "No activation keyword found."
        
        # Remove activation word
        clean_command = self._clean_activation(text)
        
        if not clean_command.strip():
            return "Please specify a command after the activation word."
        
        # Try exact matches first
        for command in self.commands:
            if command.can_execute(clean_command):
                result = command.execute(clean_command)
                self.stats['exact_matches'] += 1
                return f"✓ {result}"
        
        # Try fuzzy matching
        fuzzy_result = self.fuzzy_matcher.find_command_match(clean_command, self.commands)
        
        if fuzzy_result:
            command, confidence, matched_keyword = fuzzy_result
            result = command.execute(clean_command)
            self.stats['fuzzy_matches'] += 1
            
            if confidence < 80.0:
                # Show confidence for lower matches
                return f"🔍 (matched '{matched_keyword}' {confidence:.0f}%) {result}"
            else:
                return f"✓ {result}"
        
        # No match found, provide suggestions
        self.stats['failed_matches'] += 1
        suggestions = self.fuzzy_matcher.suggest_corrections(clean_command, self.commands, max_suggestions=3)
        
        if suggestions:
            suggestion_text = ", ".join(f"'{s}'" for s in suggestions[:2])
            return f"❌ Command '{clean_command}' not recognized. Did you mean: {suggestion_text}?"
        else:
            return f"❌ Command '{clean_command}' not recognized. Say 'help' for available commands."
    
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
    
    def get_stats(self) -> Dict[str, int]:
        """Get command processing statistics"""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset statistics"""
        for key in self.stats:
            self.stats[key] = 0