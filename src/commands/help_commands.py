from .base import BaseCommand

class HelpCommand(BaseCommand):
    """Command to show available commands"""
    
    def __init__(self, command_processor=None):
        keywords = ["ayuda", "help", "comandos", "commands", "qué puedes hacer", "what can you do"]
        description = "Shows available commands and how to use them"
        super().__init__(keywords, description)
        self.command_processor = command_processor
    
    def set_processor(self, processor):
        """Set the command processor reference"""
        self.command_processor = processor
    
    def execute(self, command_text: str) -> str:
        if not self.command_processor:
            return "Help system not properly initialized"
        
        commands_info = self.command_processor.list_commands()
        
        help_text = "=== Available Commands ===\n"
        help_text += f"Activation words: {', '.join(self.command_processor.activation_words)}\n\n"
        
        for i, cmd_info in enumerate(commands_info, 1):
            keywords = ", ".join(cmd_info["keywords"][:3])  # Show first 3 keywords
            if len(cmd_info["keywords"]) > 3:
                keywords += "..."
            
            help_text += f"{i}. Keywords: {keywords}\n"
            help_text += f"   Description: {cmd_info['description']}\n\n"
        
        help_text += "Examples:\n"
        help_text += "- 'Furina, qué hora es' - Get current time\n"
        help_text += "- 'Furina, abre navegador' - Open browser\n"
        help_text += "- 'Furina, fecha de hoy' - Get current date\n"
        help_text += "- 'Furina, subir volumen' - Increase volume\n"
        
        return help_text

class GreetingCommand(BaseCommand):
    """Command for greetings and basic interactions"""
    
    def __init__(self):
        keywords = ["hola", "hello", "hi", "buenos días", "good morning", "buenas tardes", "good afternoon", "buenas noches", "good evening"]
        description = "Responds to greetings"
        super().__init__(keywords, description)
    
    def execute(self, command_text: str) -> str:
        command_lower = command_text.lower()
        
        if any(word in command_lower for word in ["hola", "hello", "hi"]):
            return "¡Hola! I'm your voice assistant. Say 'ayuda' or 'help' to see available commands."
        
        elif any(word in command_lower for word in ["buenos días", "good morning"]):
            return "¡Buenos días! How can I help you today?"
        
        elif any(word in command_lower for word in ["buenas tardes", "good afternoon"]):
            return "¡Buenas tardes! What can I do for you?"
        
        elif any(word in command_lower for word in ["buenas noches", "good evening"]):
            return "¡Buenas noches! How may I assist you this evening?"
        
        return "Hello! I'm here to help. Try saying 'help' to see what I can do."