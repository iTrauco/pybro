"""
🔍 Chrome Profile Scanner
Handles detection and management of Chrome profiles with enhanced profile information
"""
# Standard library imports
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, NamedTuple, Union, Any

# Third-party imports
from rich.console import Console
from rich.logging import RichHandler

# Local imports - using relative imports for package structure
from ..config.settings import (
    CHROME_CONFIG_PATH,
    CLI_VERSION,
    CLI_TITLE
)

# Configure logging
logging.basicConfig(
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

# Initialize logger and console
log = logging.getLogger("chrome_scanner")
console = Console()

class ChromeProfile(NamedTuple):
    """Structure to hold Chrome profile information"""
    name: str           # Directory name (e.g., "Profile 1")
    email: Optional[str]
    is_local: bool
    last_used: Optional[str]
    profile_path: Path
    custom_name: Optional[str]  # The user-set profile name
    preferences: Dict[str, Any]  # Raw preferences data

class ChromeProfileScanner:
    """Enhanced scanner for Chrome profiles with local profile support"""
    
    def get_chrome_profiles(self) -> List[str]:
        """
        🔎 Scans filesystem for all Chrome profiles
        Returns: List of profile directory names
        """
        try:
            profiles = []
            if CHROME_CONFIG_PATH.exists():
                # Add Default profile if it exists
                default_profile = CHROME_CONFIG_PATH / "Default"
                if default_profile.is_dir():
                    profiles.append("Default")
                
                # Add numbered profiles
                for profile in CHROME_CONFIG_PATH.iterdir():
                    if profile.is_dir() and profile.name.startswith("Profile "):
                        profiles.append(profile.name)
            
            log.debug(f"Found {len(profiles)} Chrome profiles")
            return sorted(profiles, key=self._profile_sort_key)
        except Exception as e:
            log.error(f"Error scanning profiles: {e}")
            return []

    def _profile_sort_key(self, profile_name: str) -> tuple:
        """Custom sort key for profile names"""
        if profile_name == "Default":
            return (0, 0)
        try:
            num = int(profile_name.split()[1])
            return (1, num)
        except (IndexError, ValueError):
            return (2, profile_name)

    def extract_profile_info(self, preferences_path: Path) -> Dict[str, Any]:
        """
        📋 Extracts detailed profile information from preferences file
        Args:
            preferences_path: Path to Chrome preferences file
        Returns: Dictionary containing profile information
        """
        try:
            with open(preferences_path, "r", encoding='utf-8') as file:
                data = json.load(file)
                
                # Extract account info
                account_info = data.get("account_info", [{}])[0]
                email = account_info.get("email")
                
                # Extract profile info
                profile_info = data.get("profile", {})
                custom_name = profile_info.get("name")
                last_used = profile_info.get("last_used")
                
                # Get additional sync info if available
                sync_info = data.get("google", {}).get("chrome_sync", {})
                if not custom_name and sync_info:
                    custom_name = sync_info.get("profile_name")
                
                return {
                    'email': email,
                    'custom_name': custom_name,
                    'last_used': last_used,
                    'preferences': data,  # Store full preferences for potential future use
                    'local_profile_exists': bool(custom_name and not email)
                }
                
        except Exception as e:
            log.error(f"Error reading preferences file {preferences_path}: {e}")
            return {}

    def get_detailed_profiles(self) -> Dict[str, ChromeProfile]:
        """
        👥 Gets detailed information about all Chrome profiles
        Returns: Dictionary mapping profile names to ChromeProfile objects
        """
        detailed_profiles = {}
        
        try:
            for profile_name in self.get_chrome_profiles():
                profile_path = CHROME_CONFIG_PATH / profile_name
                preferences_path = profile_path / "Preferences"
                
                if preferences_path.exists():
                    info = self.extract_profile_info(preferences_path)
                    
                    detailed_profiles[profile_name] = ChromeProfile(
                        name=profile_name,
                        email=info.get('email'),
                        is_local=info.get('local_profile_exists', False),
                        last_used=info.get('last_used'),
                        profile_path=profile_path,
                        custom_name=info.get('custom_name'),
                        preferences=info.get('preferences', {})
                    )
                else:
                    # Handle profiles without preference files as local profiles
                    detailed_profiles[profile_name] = ChromeProfile(
                        name=profile_name,
                        email=None,
                        is_local=True,
                        last_used=None,
                        profile_path=profile_path,
                        custom_name=None,
                        preferences={}
                    )
            
            return detailed_profiles
            
        except Exception as e:
            log.error(f"Error getting detailed profiles: {e}")
            return {}

    def display_all_profiles(self) -> None:
        """
        📊 Displays all profiles with their status
        """
        profiles = self.get_detailed_profiles()
        
        if not profiles:
            console.print("❌ No Chrome profiles found!", style="bold red")
            return

        # Display signed-in profiles
        console.print("\n🔐 Signed-in Profiles:", style="bold blue")
        signed_in = [p for p in profiles.values() if p.email]
        if signed_in:
            for profile in signed_in:
                # Format email with username and domain highlighted differently
                if profile.email:
                    username, domain = profile.email.split('@')
                    email_display = f"[bold green]{username}[/bold green]@[bold]{domain}[/bold]"
                    profile_info = f"[cyan]{profile.name}[/cyan]: {email_display}"
                    if profile.custom_name:
                        profile_info += f" - [blue]{profile.custom_name}[/blue]"
                    console.print(f"  • {profile_info}")
        else:
            console.print("  No signed-in profiles found", style="italic")

        # Display local profiles
        console.print("\n📂 Local Profiles:", style="bold green")
        local = [p for p in profiles.values() if p.is_local]
        if local:
            for profile in local:
                profile_info = f"[cyan]{profile.name}[/cyan]"
                if profile.custom_name:
                    profile_info += f" [yellow](Local Profile - {profile.custom_name})[/yellow]"
                else:
                    profile_info += " [yellow](Local Profile)[/yellow]"
                console.print(f"  • {profile_info}")
        else:
            console.print("  No local profiles found", style="italic")

    def get_profile_users(self) -> Dict[str, str]:
        """
        📧 Legacy support: Maps profiles to emails (signed-in profiles only)
        Returns: Dictionary mapping profile names to user emails
        """
        return {
            profile.name: profile.email 
            for profile in self.get_detailed_profiles().values() 
            if profile.email
        }

# Example usage and testing code
if __name__ == "__main__":
    try:
        scanner = ChromeProfileScanner()
        console.print(f"\n{CLI_TITLE} v{CLI_VERSION} - Profile Scanner", style="bold blue")
        scanner.display_all_profiles()
        
        # Show detailed information
        console.print("\n📋 Detailed Profile Information:", style="bold magenta")
        for profile in scanner.get_detailed_profiles().values():
            console.print("\nProfile Details:", style="bold")
            console.print(f"  Directory: [cyan]{profile.name}[/cyan]")
            console.print(f"  Type: {'[yellow]Local[/yellow]' if profile.is_local else '[blue]Signed-in[/blue]'}")
            if profile.email:
                username, domain = profile.email.split('@')
                email_display = f"[bold green]{username}[/bold green]@[bold]{domain}[/bold]"
                console.print(f"  Email: {email_display}")
            if profile.custom_name:
                console.print(f"  Profile Name: [blue]{profile.custom_name}[/blue]")
            if profile.last_used:
                console.print(f"  Last Used: [italic]{profile.last_used}[/italic]")
                
    except Exception as e:
        log.error(f"Scanner test error: {e}")
        console.print(f"\n❌ Error: {e}", style="bold red")