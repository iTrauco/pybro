# 📄 ./helpers/alias_creator.py

"""
🏷️ Chrome Alias Creator Helper
Manages creation and installation of Chrome profile aliases
"""
from pathlib import Path
from typing import Optional
import logging
from rich.console import Console
from config.settings import CHROME_BINARY, ZSHRC_PATH

console = Console()
log = logging.getLogger("alias_creator")

class ChromeAliasManager:
    """Handles creation and management of Chrome aliases"""

    @staticmethod
    def create_chrome_alias(alias_name: str, profile: str, url: Optional[str] = None) -> str:
        """
        🔨 Creates a Chrome alias command matching the system format
        Args:
            alias_name: Name for the new alias
            profile: Chrome profile directory name
            url: Optional URL to open
        Returns: Formatted alias command
        """
        # Use absolute path to Chrome binary
        chrome_path = "/usr/bin/google-chrome"
        
        # Build command with exact required format
        if url:
            cmd = f'{chrome_path} --profile-directory=\\"{profile}\\" --new-window {url}'
        else:
            cmd = f'{chrome_path} --profile-directory=\\"{profile}\\" --new-window'
            
        # Create the complete alias command
        alias_cmd = f'alias {alias_name}="{cmd}"'
        
        # Log the created command for verification
        log.debug(f"Created alias command: {alias_cmd}")
        
        return alias_cmd

    @staticmethod
    def add_alias_to_zshrc(alias_cmd: str) -> bool:
        """
        💾 Saves alias to .zshrc file
        Args:
            alias_cmd: Formatted alias command to save
        Returns: Success status
        """
        try:
            if ZSHRC_PATH.exists():
                # Check for existing alias
                content = Path(ZSHRC_PATH).read_text()
                if alias_cmd in content:
                    console.print("⚠️ Alias already exists!", style="yellow")
                    return False
            
            # Add new alias with description
            with open(ZSHRC_PATH, "a") as f:
                f.write(f"\n# 🌐 Chrome Profile Alias - Created by Chrome Profile Manager\n")
                f.write(f"{alias_cmd}\n")
            
            # Show the created command for verification
            console.print("\n✅ Created alias:", style="green")
            console.print(f"{alias_cmd}", style="blue")
            
            return True
            
        except Exception as e:
            console.print(f"❌ Error adding alias: {e}", style="bold red")
            return False