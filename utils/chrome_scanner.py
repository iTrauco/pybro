# 📄 ./utils/chrome_scanner.py
"""
🔍 Chrome Profile Scanner
Handles all Chrome profile detection and information extraction
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
from rich.console import Console
from config.settings import CHROME_CONFIG_PATH

console = Console()

class ChromeProfileScanner:
    """Scans and extracts information about Chrome profiles"""
    
    @staticmethod
    def get_chrome_profiles() -> List[str]:
        """
        🔎 Scans filesystem for Chrome profiles
        Returns: List of profile directory names
        """
        try:
            profiles = []
            if CHROME_CONFIG_PATH.exists():
                for profile in CHROME_CONFIG_PATH.iterdir():
                    if profile.is_dir() and profile.name.startswith("Profile "):
                        profiles.append(profile.name)
            return profiles
        except Exception as e:
            console.print(f"⚠️ Error scanning profiles: {e}", style="bold red")
            return []

    @staticmethod
    def extract_user_email(preferences_path: Path) -> Optional[str]:
        """
        📧 Extracts user email from Chrome preferences file
        Args:
            preferences_path: Path to Chrome preferences file
        Returns: User email or None if not found
        """
        try:
            with open(preferences_path, "r") as file:
                data = json.load(file)
                return data.get("account_info", [{}])[0].get("email", None)
        except Exception as e:
            console.print(f"⚠️ Error reading preferences: {e}", style="bold red")
            return None

    def get_profile_users(self) -> Dict[str, str]:
        """
        👥 Maps Chrome profiles to their associated emails
        Returns: Dictionary mapping profile names to user emails
        """
        profile_users = {}
        for profile in self.get_chrome_profiles():
            preferences_path = CHROME_CONFIG_PATH / profile / "Preferences"
            if preferences_path.exists():
                user_email = self.extract_user_email(preferences_path)
                if user_email:
                    profile_users[profile] = user_email
        return profile_users