# 📄 ./utils/chrome_scanner.py

"""
🔍 Enhanced Chrome Profile Scanner with Custom Profile Name Support
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, NamedTuple
from rich.console import Console
from config.settings import CHROME_CONFIG_PATH

console = Console()
log = logging.getLogger("chrome_scanner")

class ChromeProfile(NamedTuple):
    """Structure to hold Chrome profile information"""
    name: str           # Directory name (e.g., "Profile 1")
    email: Optional[str]
    is_local: bool
    last_used: Optional[str]
    profile_path: Path
    custom_name: Optional[str]  # User-set profile name
    preferences: Dict    # Full preferences data for additional info

class ChromeProfileScanner:
    def get_chrome_profiles(self) -> List[str]:
        """Get list of Chrome profile directory names"""
        try:
            profiles = []
            if CHROME_CONFIG_PATH.exists():
                if (CHROME_CONFIG_PATH / "Default").is_dir():
                    profiles.append("Default")
                profiles.extend([
                    p.name for p in CHROME_CONFIG_PATH.iterdir()
                    if p.is_dir() and p.name.startswith("Profile ")
                ])
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

    def _read_preferences_file(self, preferences_path: Path) -> Dict:
        """Read and parse Chrome preferences file"""
        try:
            with open(preferences_path, "r", encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            log.error(f"Error reading preferences file {preferences_path}: {e}")
            return {}

    def extract_profile_info(self, profile_name: str) -> Optional[ChromeProfile]:
        """Extract detailed profile information"""
        try:
            profile_path = CHROME_CONFIG_PATH / profile_name
            preferences_path = profile_path / "Preferences"
            
            if not preferences_path.exists():
                return ChromeProfile(
                    name=profile_name,
                    email=None,
                    is_local=True,
                    last_used=None,
                    profile_path=profile_path,
                    custom_name="Unnamed Profile",
                    preferences={}
                )

            prefs = self._read_preferences_file(preferences_path)
            
            # Extract email from account info
            email = None
            if account_info := prefs.get("account_info", [{}]):
                email = account_info[0].get("email")

            # Get profile information
            profile_info = prefs.get("profile", {})
            custom_name = profile_info.get("name")
            
            # Additional profile data from sync preferences
            sync_info = prefs.get("google", {}).get("chrome_sync", {})
            if not custom_name and sync_info:
                custom_name = sync_info.get("profile_name")

            return ChromeProfile(
                name=profile_name,
                email=email,
                is_local=bool(custom_name and not email),
                last_used=profile_info.get("last_used"),
                profile_path=profile_path,
                custom_name=custom_name,
                preferences=prefs
            )
        except Exception as e:
            log.error(f"Error extracting profile info for {profile_name}: {e}")
            return None

    def get_detailed_profiles(self) -> Dict[str, ChromeProfile]:
        """Get detailed information about all Chrome profiles"""
        profiles = {}
        for profile_name in self.get_chrome_profiles():
            if profile_info := self.extract_profile_info(profile_name):
                profiles[profile_name] = profile_info
        return profiles

if __name__ == "__main__":
    scanner = ChromeProfileScanner()
    profiles = scanner.get_detailed_profiles()
    for profile in profiles.values():
        print(f"Profile: {profile.name}")
        print(f"Email: {profile.email}")
        print(f"Custom Name: {profile.custom_name}")
        print("---")