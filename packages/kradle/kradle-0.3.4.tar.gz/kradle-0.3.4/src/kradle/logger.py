from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.logging import RichHandler
from rich import box
import logging
import sys
from typing import Optional, Dict, Any
from datetime import datetime

class KradleLogger:
    def __init__(self):
        self.console = Console()
        self._setup_logging()
        
    def _setup_logging(self):
        """Configure logging with Rich handler for beautiful formatting"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[
                RichHandler(
                    rich_tracebacks=True,
                    markup=True,
                    show_time=False
                )
            ]
        )
        # Keep Flask debug logs clean
        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.handlers = []
        werkzeug_handler = logging.StreamHandler(sys.stdout)
        werkzeug_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(message)s',
            '%H:%M:%S'
        ))
        werkzeug_logger.addHandler(werkzeug_handler)
        werkzeug_logger.setLevel(logging.INFO)
            
    def display_startup_banner(self, config: Dict[str, Any]):
        """Display a beautiful startup banner with server information"""
        self.console.clear()
        
        # Network URLs panel
        network_info = Text()
        network_info.append(f"✨ {config.get('agent_username')} is running!\n\n", style="bold green")
        network_info.append("\n→ Local URL     ", style="white")
        network_info.append(f"http://localhost:{config.get('port')}/{config.get('agent_username')}\n", style="cyan")
        
        agent_url = config.get('agent_url', '')
        if 'pinggy.link' in agent_url:
            network_info.append("→ Network URL   ", style="white")
            network_info.append(f"{agent_url}\n", style="cyan")
        
        network_info.append("→ Visit ", style="white")
        network_info.append("http://app.kradle.ai/workbench/challenges", style="cyan underline")
        network_info.append(" to select a challenge to run your agent against\n", style="white")
        

        self.console.print(Panel(
            network_info,
            title="[white]Network",
            border_style="bright_black",
            box=box.ROUNDED,
            padding=(1, 2)
        ))
        
        
        # Control tip
        self.console.print("\n[dim]Press Ctrl+C to stop the server[/dim]")
        print()

    def log_success(self, message: str):
        """Log a success message"""
        self.console.print(f"✓ {message}", style="green")

    def log_error(self, message: str, error: Optional[Exception] = None):
        """Log an error message with optional exception details"""
        self.console.print(f"✕ {message}", style="red")
        if error:
            self.console.print(f"  → {type(error).__name__}: {str(error)}", style="red dim")

    def log_warning(self, message: str):
        """Log a warning message"""
        self.console.print(f"! {message}", style="yellow")

    def log_info(self, message: str):
        """Log an informational message"""
        self.console.print(f"○ {message}", style="blue")

    def log_debug(self, message: str):
        """Log a debug message"""
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            self.console.print(f"· {message}", style="dim")

    def log_api_call(self, method: str, endpoint: str, status: int):
        """Log an API call with color-coded status"""
        status_color = "green" if 200 <= status < 300 else "red"
        method_width = 6  # Consistent width for method
        self.console.print(
            f"  {method:<{method_width}} {endpoint} [{status_color}]{status}[/]",
            style="dim"
        )

    def on_shutdown(self):
        """Display shutdown message"""
        self.console.print("\n[yellow]Shutting down Kradle Agent Server...[/yellow]")