# 1. 📄 ./helpers/alias_creator.py (rename from alias_creator_helper.py)
"""
🏷️ Chrome Alias Creator
Manages creation and installation of Chrome profile aliases
"""
from pathlib import Path
from typing import Optional
from rich.console import Console
from config.settings import CHROME_BINARY, ZSHRC_PATH

console = Console()

class ChromeAliasManager:
    """Handles creation and management of Chrome aliases"""

    @staticmethod
    def create_chrome_alias(alias_name: str, profile: str, url: Optional[str] = None) -> str:
        """
        🔨 Creates a Chrome alias command
        Args:
            alias_name: Name for the new alias
            profile: Chrome profile directory name
            url: Optional URL to open
        Returns: Formatted alias command
        """
        chrome_cmd = f'{CHROME_BINARY} --profile-directory="{profile}"'
        if url:
            chrome_cmd += f' "{url}"'
        return f'alias {alias_name}="{chrome_cmd}"'

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
            
            # Add new alias
            with open(ZSHRC_PATH, "a") as f:
                f.write(f"\n# 🌐 Chrome Profile Alias\n{alias_cmd}\n")
            console.print("✅ Alias added successfully!", style="green")
            return True
            
        except Exception as e:
            console.print(f"❌ Error adding alias: {e}", style="bold red")
            return False
