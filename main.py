"""
🎮 Chrome Profile Manager CLI
Main entry point for the Chrome Profile Manager application with enhanced debugging
"""
import sys
import logging
from pathlib import Path
from typing import Dict, Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.logging import RichHandler
from rich.traceback import install

from helpers.alias_creator import ChromeAliasManager



# Add project root to Python path
sys.path.append(str(Path(__file__).parent))

# Import local modules
try:
    from utils.chrome_scanner import ChromeProfileScanner
    from helpers.alias_creator import ChromeAliasManager
    from config.settings import CLI_TITLE, CLI_VERSION
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("📁 Current Python Path:")
    for path in sys.path:
        print(f"  - {path}")
    sys.exit(1)

# Setup rich traceback handling
install(show_locals=True)

# Configure logging
logging.basicConfig(
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger("chrome_manager")
console = Console()

class ChromeProfileManagerCLI:
    """Main CLI application class with enhanced error handling and debugging"""
    
    def __init__(self):
        """Initialize the CLI manager with debug information"""
        log.debug("🚀 Initializing Chrome Profile Manager CLI")
        try:
            self.scanner = ChromeProfileScanner()
            self.alias_manager = ChromeAliasManager()
            log.debug("✅ Successfully initialized core components")
        except Exception as e:
            log.error(f"❌ Failed to initialize components: {e}")
            raise

    def display_main_menu(self) -> None:
        """🖥️ Displays the main interactive menu with error handling"""
        while True:
            try:
                console.clear()
                console.print(f"\n{CLI_TITLE} v{CLI_VERSION}", style="bold blue")
                console.print("\n1. 🆕 Create new Chrome profile alias with URL")
                console.print("2. 🏠 Create new Chrome profile alias (homepage only)")
                console.print("3. 📋 List current Chrome profiles")
                console.print("4. 🔍 Debug Information")
                console.print("5. 🚪 Exit")
                
                choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4", "5"])
                
                if choice == "1":
                    self.create_url_alias()
                elif choice == "2":
                    self.create_homepage_alias()
                elif choice == "3":
                    self.list_profiles()
                elif choice == "4":
                    self.show_debug_info()
                else:
                    console.print("\n👋 Goodbye!", style="bold blue")
                    break

            except Exception as e:
                log.error(f"❌ Menu error: {e}")
                console.print("\n⚠️ An error occurred. See log for details.", style="bold red")
                input("\nPress Enter to continue...")

    def create_url_alias(self) -> None:
        """📝 Creates a new Chrome profile alias with specific URL"""
        log.debug("Starting URL alias creation")
        console.clear()
        console.print("\n🆕 Create New Chrome Profile URL Alias", style="bold green")
        
        try:
            profile_users = self._get_profiles()
            if not profile_users:
                return

            profile = self._get_profile_selection(profile_users)
            alias_name = self._get_valid_alias_name()
            url = Prompt.ask("🔗 Enter URL (e.g., https://example.com)")
            
            log.debug(f"Creating alias: {alias_name} for profile: {profile} with URL: {url}")
            alias_cmd = self.alias_manager.create_chrome_alias(alias_name, profile, url)
            
            if self.alias_manager.add_alias_to_zshrc(alias_cmd):
                console.print("\n🔄 Reload your shell or run 'source ~/.zshrc'", style="italic")
            
        except Exception as e:
            log.error(f"❌ Error in create_url_alias: {e}")
            console.print(f"\n⚠️ Failed to create URL alias: {e}", style="bold red")
        finally:
            input("\nPress Enter to continue...")

    def create_homepage_alias(self) -> None:
        """📝 Creates a new Chrome profile alias for homepage"""
        log.debug("Starting homepage alias creation")
        console.clear()
        console.print("\n🆕 Create New Chrome Profile Homepage Alias", style="bold green")
        
        try:
            profile_users = self._get_profiles()
            if not profile_users:
                return

            profile = self._get_profile_selection(profile_users)
            alias_name = self._get_valid_alias_name()
            
            log.debug(f"Creating homepage alias: {alias_name} for profile: {profile}")
            alias_cmd = self.alias_manager.create_chrome_alias(alias_name, profile)
            
            if self.alias_manager.add_alias_to_zshrc(alias_cmd):
                console.print("\n🔄 Reload your shell or run 'source ~/.zshrc'", style="italic")
            
        except Exception as e:
            log.error(f"❌ Error in create_homepage_alias: {e}")
            console.print(f"\n⚠️ Failed to create homepage alias: {e}", style="bold red")
        finally:
            input("\nPress Enter to continue...")

    def list_profiles(self) -> None:
        """📋 Lists all available Chrome profiles"""
        log.debug("Listing Chrome profiles")
        console.clear()
        console.print("\n📋 Current Chrome Profiles", style="bold green")
        
        try:
            profile_users = self.scanner.get_profile_users()
            self._display_profiles(profile_users)
        except Exception as e:
            log.error(f"❌ Error listing profiles: {e}")
            console.print(f"\n⚠️ Failed to list profiles: {e}", style="bold red")
        finally:
            input("\nPress Enter to continue...")

    def show_debug_info(self) -> None:
        """🔍 Displays debug information"""
        console.clear()
        console.print("\n🔍 Debug Information", style="bold blue")
        
        try:
            # System information
            console.print("\n📂 System Paths:", style="bold green")
            for path in sys.path:
                console.print(f"  - {path}")

            # Chrome profiles
            console.print("\n👤 Chrome Profiles:", style="bold green")
            profiles = self.scanner.get_chrome_profiles()
            for profile in profiles:
                console.print(f"  - {profile}")

            # Configuration
            console.print("\n⚙️ Configuration:", style="bold green")
            from config.settings import CHROME_CONFIG_PATH, ZSHRC_PATH
            console.print(f"  Chrome Config: {CHROME_CONFIG_PATH}")
            console.print(f"  ZSHRC Path: {ZSHRC_PATH}")
            
        except Exception as e:
            log.error(f"❌ Error showing debug info: {e}")
            console.print(f"\n⚠️ Failed to show debug info: {e}", style="bold red")
        finally:
            input("\nPress Enter to continue...")

    def _get_profiles(self) -> Optional[Dict[str, str]]:
        """Helper method to get and validate profiles"""
        try:
            profile_users = self.scanner.get_profile_users()
            if not self._display_profiles(profile_users):
                return None
            return profile_users
        except Exception as e:
            log.error(f"❌ Error getting profiles: {e}")
            return None

    def _display_profiles(self, profile_users: Dict[str, str]) -> bool:
        """Helper method to display profile list with error handling"""
        try:
            if not profile_users:
                console.print("\n❌ No Chrome profiles found!", style="bold red")
                return False
            
            console.print("\n📊 Available Profiles:", style="bold blue")
            for i, (profile, email) in enumerate(profile_users.items(), 1):
                console.print(f"{i}. {profile}: {email}")
            return True
        except Exception as e:
            log.error(f"❌ Error displaying profiles: {e}")
            return False

    def _get_profile_selection(self, profile_users: Dict[str, str]) -> str:
        """Helper method to get profile selection with validation"""
        while True:
            try:
                profile_index = int(Prompt.ask("\n👆 Select profile number", default="1"))
                if 1 <= profile_index <= len(profile_users):
                    return list(profile_users.keys())[profile_index - 1]
                console.print("⚠️ Invalid profile number", style="yellow")
            except ValueError:
                console.print("⚠️ Please enter a valid number", style="yellow")

    def _get_valid_alias_name(self) -> str:
        """Helper method to get and validate alias name"""
        while True:
            alias_name = Prompt.ask("🏷️ Enter alias name (e.g., work-chrome)")
            if alias_name and alias_name.isalnum() or "-" in alias_name:
                return alias_name
            console.print("⚠️ Invalid alias name. Use letters, numbers, and hyphens only.", style="yellow")

if __name__ == "__main__":
    try:
        log.info("🚀 Starting Chrome Profile Manager")
        cli = ChromeProfileManagerCLI()
        cli.display_main_menu()
    except KeyboardInterrupt:
        console.print("\n\n👋 Goodbye!", style="bold blue")
    except Exception as e:
        log.error(f"❌ Fatal error: {e}")
        console.print(f"\n❌ An error occurred: {e}", style="bold red")
        sys.exit(1)