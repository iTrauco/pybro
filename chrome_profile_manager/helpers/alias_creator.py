"""
🏷️ Chrome Alias Creator Helper
Manages creation and installation of Chrome profile aliases with consistent quote handling
"""
# Standard library imports
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
import subprocess
import urllib.parse

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
    def clean_url(url: str) -> str:
        """
        Properly escapes and formats URL for shell usage
        Args:
            url: The URL to clean and escape
        Returns: Properly escaped URL string
        """
        try:
            # First, ensure the URL is properly encoded
            parsed = urllib.parse.urlparse(url)
            
            # Reconstruct URL with properly encoded query parameters
            clean_url = parsed._replace(
                query=urllib.parse.quote_plus(parsed.query, safe='=&')
            ).geturl()
            
            # Return URL with proper quoting
            return f'"{clean_url}"'
        except Exception as e:
            log.error(f"Error cleaning URL: {e}")
            raise

    @staticmethod
    def create_chrome_alias(alias_name: str, profile: str, url: Optional[str] = None) -> str:
        """
        🔨 Creates a Chrome alias command with consistent quote handling
        Args:
            alias_name: Name for the new alias
            profile: Chrome profile directory name
            url: Optional URL to open
        Returns: Formatted alias command
        """
        try:
            # Ensure consistent profile directory formatting with escaped quotes
            profile_part = f'--profile-directory=\\"Profile {profile.split()[-1]}\\"'
            
            # Build the base command
            chrome_cmd_parts = [
                CHROME_BINARY,
                profile_part,
                '--new-window'
            ]
            
            # Add URL if provided
            if url:
                # Ensure URL has protocol
                if not url.startswith(('http://', 'https://')):
                    url = f'https://{url}'
                
                # Add URL with proper quotes
                chrome_cmd_parts.append(f'"{url}"')
            
            # Join command parts
            chrome_cmd = ' '.join(chrome_cmd_parts)
            
            # Create the complete alias command with outer double quotes
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
    def validate_zsh_syntax() -> bool:
        """
        Validates zsh syntax after adding new alias
        Returns: True if syntax is valid, False otherwise
        """
        try:
            result = subprocess.run(
                ['zsh', '-n', str(ZSHRC_PATH)],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            log.error(f"Error validating zsh syntax: {e}")
            return False

    @staticmethod
    def add_alias_to_zshrc(alias_cmd: str) -> bool:
        """
        💾 Saves alias to .zshrc file with validation
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
            
            # Validate the new alias
            if not ChromeAliasManager.validate_zsh_syntax():
                log.warning("⚠️ Warning: New alias might have syntax issues")
                console.print("⚠️ Warning: New alias might have syntax issues", style="yellow")
            
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
        
        # Test cases
        test_cases = [
            # Simple URL
            ("test-linkedin", "1", "https://linkedin.com"),
            
            # Complex URL with query parameters
            ("test-gcp", "12", "https://console.cloud.google.com/functions/list?referrer=search&hl=en&project=test-project"),
            
            # URL with special characters
            ("test-special", "2", "https://example.com/path?name=test&query=hello world&special=!@#$"),
        ]
        
        for alias_name, profile, url in test_cases:
            test_alias = manager.create_chrome_alias(
                alias_name=alias_name,
                profile=profile,
                url=url
            )
            console.print(f"\n🧪 Testing alias creation for {alias_name}:", style="bold blue")
            console.print(f"Generated Command: {test_alias}", style="green")
        
        # List existing aliases
        console.print("\n📋 Existing Chrome Aliases:", style="bold blue")
        for alias in manager.list_chrome_aliases():
            console.print(f"  {alias}", style="cyan")
            
    except Exception as e:
        console.print(f"\n❌ Test Error: {e}", style="bold red")