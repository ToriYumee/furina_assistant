from .base import BaseCommand
import platform
import psutil
from datetime import datetime, timedelta

class StatsCommand(BaseCommand):
    """Command to show assistant statistics"""
    
    def __init__(self, command_processor=None):
        keywords = ["estadísticas", "stats", "statistics", "rendimiento", "performance"]
        description = "Shows assistant usage statistics"
        super().__init__(keywords, description)
        self.command_processor = command_processor
    
    def set_processor(self, processor):
        """Set the command processor reference"""
        self.command_processor = processor
    
    def execute(self, command_text: str) -> str:
        if not self.command_processor:
            return "Statistics not available"
        
        stats = self.command_processor.get_stats()
        
        if stats['total_commands'] == 0:
            return "No commands processed yet"
        
        exact_percent = (stats['exact_matches'] / stats['total_commands']) * 100
        fuzzy_percent = (stats['fuzzy_matches'] / stats['total_commands']) * 100
        failed_percent = (stats['failed_matches'] / stats['total_commands']) * 100
        
        result = "=== Assistant Statistics ===\n"
        result += f"Total commands: {stats['total_commands']}\n"
        result += f"Exact matches: {stats['exact_matches']} ({exact_percent:.1f}%)\n"
        result += f"Fuzzy matches: {stats['fuzzy_matches']} ({fuzzy_percent:.1f}%)\n"
        result += f"Failed matches: {stats['failed_matches']} ({failed_percent:.1f}%)\n"
        result += f"Success rate: {100 - failed_percent:.1f}%"
        
        return result

class SystemInfoCommand(BaseCommand):
    """Command to show system information"""
    
    def __init__(self):
        keywords = ["sistema", "system", "info", "información del sistema", "system info"]
        description = "Shows system information"
        super().__init__(keywords, description)
    
    def execute(self, command_text: str) -> str:
        try:
            # Basic system info
            system = platform.system()
            release = platform.release()
            version = platform.version()
            machine = platform.machine()
            processor = platform.processor()
            
            # Memory info
            memory = psutil.virtual_memory()
            memory_total = memory.total / (1024**3)  # GB
            memory_used = memory.used / (1024**3)   # GB
            memory_percent = memory.percent
            
            # CPU info
            cpu_count = psutil.cpu_count()
            cpu_percent = psutil.cpu_percent(interval=1)
            
            result = "=== System Information ===\n"
            result += f"OS: {system} {release}\n"
            result += f"Machine: {machine}\n"
            result += f"Processor: {processor[:50]}...\n" if len(processor) > 50 else f"Processor: {processor}\n"
            result += f"CPU Cores: {cpu_count}\n"
            result += f"CPU Usage: {cpu_percent}%\n"
            result += f"Memory: {memory_used:.1f}GB / {memory_total:.1f}GB ({memory_percent}%)"
            
            return result
            
        except Exception as e:
            return f"Error getting system info: {e}"

class UptimeCommand(BaseCommand):
    """Command to show system uptime"""
    
    def __init__(self):
        keywords = ["uptime", "tiempo encendido", "cuánto tiempo", "how long"]
        description = "Shows system uptime"
        super().__init__(keywords, description)
        self.start_time = datetime.now()
    
    def execute(self, command_text: str) -> str:
        try:
            # System uptime
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            system_uptime = datetime.now() - boot_time
            
            # Assistant uptime
            assistant_uptime = datetime.now() - self.start_time
            
            def format_timedelta(td):
                days = td.days
                hours, remainder = divmod(td.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                parts = []
                if days > 0:
                    parts.append(f"{days} day{'s' if days != 1 else ''}")
                if hours > 0:
                    parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
                if minutes > 0:
                    parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
                if not parts and seconds > 0:
                    parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
                
                return ", ".join(parts) if parts else "less than a minute"
            
            result = "=== Uptime Information ===\n"
            result += f"System uptime: {format_timedelta(system_uptime)}\n"
            result += f"Assistant uptime: {format_timedelta(assistant_uptime)}"
            
            return result
            
        except Exception as e:
            return f"Error getting uptime: {e}"

class TestFuzzyCommand(BaseCommand):
    """Command to test fuzzy matching capabilities"""
    
    def __init__(self):
        keywords = ["test fuzzy", "probar fuzzy", "test detection", "probar detección"]
        description = "Tests fuzzy matching detection"
        super().__init__(keywords, description)
    
    def execute(self, command_text: str) -> str:
        examples = [
            "Try saying these with intentional errors:",
            "• 'abre navgador' (instead of 'navegador')",
            "• 'que ora es' (instead of 'qué hora es')",
            "• 'calculaora' (instead of 'calculadora')",
            "• 'subr volumen' (instead of 'subir volumen')",
            "• 'ayua' (instead of 'ayuda')"
        ]
        
        return "\n".join(examples)