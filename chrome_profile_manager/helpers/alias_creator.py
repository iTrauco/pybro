"""
🏷️ Chrome Alias Creator Helper
Manages creation and installation of Chrome profile aliases
"""
# Standard library imports
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
import subprocess
import shlex

# Third-party imports
from rich.console import Console
from rich.logging import RichHandler

# Local imports - using relative imports
from ..config.settings import (
    CHROME_BINARY,
    ZSHRC_PATH
)

# Configure logging
logging.basicConfig(
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

# Initialize logger and console
log = logging.getLogger("alias_creator")
console = Console()

class ChromeAliasManager:
    """Handles creation and management of Chrome aliases"""

    @staticmethod
    def create_chrome_alias(alias_name: str, profile: str, url: Optional[str] = None) -> str:
        """
        🔨 Creates a Chrome alias command with exact quoting format
        Args:
            alias_name: Name for the new alias
            profile: Chrome profile directory name
            url: Optional URL to open
        Returns: Formatted alias command
        """
        try:
            # Start with the basic command
            chrome_cmd = f'{CHROME_BINARY} --profile-directory=\\"Profile {profile.split()[-1]}\\" --new-window'
            
            # Add URL if provided
            if url:
                if not url.startswith(('http://', 'https://')):
                    url = f'https://{url}'
                chrome_cmd = f'{chrome_cmd} "{url}"'
            else:
                chrome_cmd = f'{chrome_cmd} \\'  # Add backslash if no URL
            
            # Create the complete alias command
            alias_cmd = f'alias {alias_name}="{chrome_cmd}"'
            
            log.debug(f"Created alias command: {alias_cmd}")
            return alias_cmd
            
        except Exception as e:
            log.error(f"Error creating alias command: {e}")
            raise

    @staticmethod
    def validate_alias_name(alias_name: str) -> bool:
        """
        ✅ Validates the alias name
        Args:
            alias_name: Name to validate
        Returns: True if valid, False otherwise
        """
        # Check if alias name is valid (letters, numbers, hyphens only)
        return bool(alias_name and alias_name.replace("-", "").isalnum())

    @staticmethod
    def check_existing_alias(alias_name: str) -> bool:
        """
        🔍 Checks if an alias already exists in .zshrc
        Args:
            alias_name: Name to check
        Returns: True if exists, False otherwise
        """
        try:
            if ZSHRC_PATH.exists():
                content = Path(ZSHRC_PATH).read_text()
                return f"alias {alias_name}=" in content
            return False
        except Exception as e:
            log.error(f"Error checking existing alias: {e}")
            return False

    @staticmethod
    def add_alias_to_zshrc(alias_cmd: str) -> bool:
        """
        💾 Saves alias to .zshrc file
        Args:
            alias_cmd: Formatted alias command to save
        Returns: Success status
        """
        try:
            # Extract alias name for checking
            alias_name = alias_cmd.split('=')[0].split()[1]
            
            if ZSHRC_PATH.exists():
                # Check for existing alias
                if ChromeAliasManager.check_existing_alias(alias_name):
                    console.print("⚠️ Alias already exists!", style="yellow")
                    return False
            
            # Add new alias with description and ensure proper formatting
            with open(ZSHRC_PATH, "a") as f:
                f.write("\n# 🌐 Chrome Profile Alias - Created by PyBro CLI")
                f.write(f"\n{alias_cmd}\n")
            
            # Show success message with command preview
            console.print("✅ Added alias to .zshrc:", style="green")
            console.print(f"  {alias_cmd}", style="blue")
            
            # Attempt to reload shell configuration
            ChromeAliasManager._try_reload_shell()
            
            return True
            
        except Exception as e:
            log.error(f"❌ Error adding alias: {e}")
            console.print(f"❌ Error adding alias: {e}", style="bold red")
            return False

    @staticmethod
    def _try_reload_shell() -> None:
        """
        🔄 Attempts to reload shell configuration
        """
        try:
            # Try to source .zshrc in the current shell
            subprocess.run(["zsh", "-c", "source ~/.zshrc"], 
                         capture_output=True, 
                         text=True,
                         check=False)
            log.debug("Shell configuration reload attempted")
        except Exception as e:
            log.debug(f"Shell reload attempt failed: {e}")
            # Failure to reload is not critical, just continue

    @staticmethod
    def remove_alias(alias_name: str) -> bool:
        """
        🗑️ Removes an alias from .zshrc
        Args:
            alias_name: Name of alias to remove
        Returns: Success status
        """
        try:
            if not ZSHRC_PATH.exists():
                console.print("⚠️ .zshrc file not found!", style="yellow")
                return False

            # Read current content
            content = Path(ZSHRC_PATH).read_text().splitlines()
            new_content = []
            skip_next = False
            removed = False

            # Process lines
            for line in content:
                if skip_next:
                    skip_next = False
                    continue
                if f"alias {alias_name}=" in line:
                    # Skip this line and the comment line above it
                    if new_content and "# 🌐 Chrome Profile Alias" in new_content[-1]:
                        new_content.pop()
                    removed = True
                    continue
                if "# 🌐 Chrome Profile Alias" in line:
                    skip_next = True
                    continue
                new_content.append(line)

            if removed:
                # Write updated content
                Path(ZSHRC_PATH).write_text('\n'.join(new_content) + '\n')
                console.print(f"✅ Removed alias: {alias_name}", style="green")
                ChromeAliasManager._try_reload_shell()
                return True
            else:
                console.print(f"⚠️ Alias {alias_name} not found!", style="yellow")
                return False

        except Exception as e:
            log.error(f"Error removing alias: {e}")
            console.print(f"❌ Error removing alias: {e}", style="bold red")
            return False

    @staticmethod
    def list_chrome_aliases() -> List[str]:
        """
        📋 Lists all Chrome profile aliases
        Returns: List of alias commands
        """
        try:
            if not ZSHRC_PATH.exists():
                return []

            aliases = []
            content = Path(ZSHRC_PATH).read_text().splitlines()
            
            for line in content:
                if line.startswith('alias ') and CHROME_BINARY in line:
                    aliases.append(line)
            
            return aliases
            
        except Exception as e:
            log.error(f"Error listing aliases: {e}")
            return []

# Example usage and testing code
if __name__ == "__main__":
    try:
        # Test alias creation
        manager = ChromeAliasManager()
        
        # Example: Create and add a test alias
        test_alias = manager.create_chrome_alias(
            alias_name="test-chrome",
            profile="Profile 1",
            url="https://example.com"
        )
        
        console.print("\n🧪 Testing Alias Creation:", style="bold blue")
        console.print(f"Generated Command: {test_alias}", style="green")
        
        # List existing aliases
        console.print("\n📋 Existing Chrome Aliases:", style="bold blue")
        for alias in manager.list_chrome_aliases():
            console.print(f"  {alias}", style="cyan")
            
    except Exception as e:
        console.print(f"\n❌ Test Error: {e}", style="bold red")