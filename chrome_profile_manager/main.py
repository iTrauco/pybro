"""
🎮 Chrome Profile Manager CLI
Main entry point for the Chrome Profile Manager application with enhanced debugging
"""
# Standard library imports
import sys
import logging
from pathlib import Path
from typing import Dict, Optional

# Third-party imports
from rich.console import Console
from rich.prompt import Prompt
from rich.logging import RichHandler
from rich.traceback import install

# Local module imports - using relative imports
from .utils.chrome_scanner import ChromeProfileScanner, ChromeProfile
from .helpers.alias_creator import ChromeAliasManager
from .config.settings import (
   CLI_TITLE,
   CLI_VERSION,
   CHROME_CONFIG_PATH,
   ZSHRC_PATH
)

# Add project root to Python path (if needed)
sys.path.append(str(Path(__file__).parent))

# Setup rich traceback handling
install(show_locals=True)

# Configure logging
logging.basicConfig(
   level="DEBUG",
   format="%(message)s",
   datefmt="[%X]",
   handlers=[RichHandler(rich_tracebacks=True)]
)

# Initialize logger and console
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
            # Ask if user wants to include local profiles
            include_local = Prompt.ask(
                "\nInclude local profiles?",
                choices=["y", "n"],
                default="y"
            ) == "y"
            
            profile = self._get_profile_selection(include_local)
            if not profile:
                console.print("⚠️ No profile selected", style="yellow")
                return
                
            alias_name = self._get_valid_alias_name()
            url = Prompt.ask("🔗 Enter URL (e.g., https://example.com)")
            
            # Ensure URL has protocol
            if url and not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            log.debug(f"Creating alias: {alias_name} for profile: {profile.name} with URL: {url}")
            
            # Use the exact profile directory name
            alias_cmd = self.alias_manager.create_chrome_alias(
                alias_name=alias_name,
                profile=profile.name,
                url=url
            )
            
            if self.alias_manager.add_alias_to_zshrc(alias_cmd):
                profile_type = "local" if profile.is_local else f"signed-in ({profile.email})"
                console.print(f"\n✅ Created alias for {profile_type} profile", style="green")
                console.print(f"✅ Command created: {alias_cmd}", style="dim")
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
            include_local = Prompt.ask(
                "\nInclude local profiles?",
                choices=["y", "n"],
                default="y"
            ) == "y"
            
            profile = self._get_profile_selection(include_local)
            if not profile:
                console.print("⚠️ No profile selected", style="yellow")
                return
            
            alias_name = self._get_valid_alias_name()
            
            log.debug(f"Creating homepage alias: {alias_name} for profile: {profile.name}")
            alias_cmd = self.alias_manager.create_chrome_alias(alias_name, profile.name)
            
            if self.alias_manager.add_alias_to_zshrc(alias_cmd):
                profile_type = "local" if profile.is_local else f"signed-in ({profile.email})"
                console.print(f"\n✅ Created alias for {profile_type} profile", style="green")
                console.print("\n🔄 Reload your shell or run 'source ~/.zshrc'", style="italic")
            
        except Exception as e:
            log.error(f"❌ Error in create_homepage_alias: {e}")
            console.print(f"\n⚠️ Failed to create homepage alias: {e}", style="bold red")
        finally:
            input("\nPress Enter to continue...")

    def list_profiles(self) -> None:
        """Enhanced profile listing with detailed information"""
        log.debug("Listing Chrome profiles with enhanced information")
        console.clear()
        console.print("\n📋 Chrome Profiles Overview", style="bold green")
        
        try:
            profiles = self.scanner.get_detailed_profiles()
            
            # Display signed-in profiles
            console.print("\n🔐 Signed-in Profiles:", style="bold blue")
            signed_in = [p for p in profiles.values() if p.email]
            if signed_in:
                for profile in signed_in:
                    profile_info = f"[cyan]{profile.name}[/cyan]"
                    if profile.email:
                        username, domain = profile.email.split('@')
                        profile_info += f" ([bold green]{username}[/bold green]@[bold]{domain}[/bold])"
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
            
            # Show detailed information if requested
            if Prompt.ask("\nShow detailed information?", choices=["y", "n"], default="n") == "y":
                console.print("\n📋 Detailed Profile Information:", style="bold magenta")
                for profile in profiles.values():
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
            profiles = self.scanner.get_detailed_profiles()
            for profile in profiles.values():
                profile_type = "Local" if profile.is_local else f"Signed-in ({profile.email})"
                console.print(f"  - [cyan]{profile.name}[/cyan] [{profile_type}]")

            # Configuration
            console.print("\n⚙️ Configuration:", style="bold green")
            console.print(f"  Chrome Config: {CHROME_CONFIG_PATH}")
            console.print(f"  ZSHRC Path: {ZSHRC_PATH}")
            
        except Exception as e:
            log.error(f"❌ Error showing debug info: {e}")
            console.print(f"\n⚠️ Failed to show debug info: {e}", style="bold red")
        finally:
            input("\nPress Enter to continue...")

    def _get_profile_selection(self, include_local: bool = True) -> Optional[ChromeProfile]:
        """Enhanced profile selection with detailed profile information"""
        while True:
            try:
                profiles = self.scanner.get_detailed_profiles()
                
                # Filter profiles based on include_local
                if not include_local:
                    profiles = {k: v for k, v in profiles.items() if not v.is_local}
                
                if not profiles:
                    console.print("⚠️ No suitable profiles found!", style="yellow")
                    return None
                
                # Display available profiles
                console.print("\n📊 Available Profiles:", style="bold blue")
                for i, (_, profile) in enumerate(profiles.items(), 1):
                    # Format the profile display
                    if profile.is_local:
                        profile_info = f"[cyan]{profile.name}[/cyan]"
                        if profile.custom_name:
                            profile_info += f" [yellow](Local Profile - {profile.custom_name})[/yellow]"
                        else:
                            profile_info += " [yellow](Local Profile)[/yellow]"
                    else:
                        profile_info = f"[cyan]{profile.name}[/cyan]"
                        if profile.email:
                            username, domain = profile.email.split('@')
                            profile_info += f" ([bold green]{username}[/bold green]@[bold]{domain}[/bold])"
                            if profile.custom_name:
                                profile_info += f" - [blue]{profile.custom_name}[/blue]"
                    
                    console.print(f"{i}. {profile_info}")
                
                profile_index = int(Prompt.ask("\n👆 Select profile number", default="1"))
                if 1 <= profile_index <= len(profiles):
                    return list(profiles.values())[profile_index - 1]
                
                console.print("⚠️ Invalid profile number", style="yellow")
                
            except ValueError as e:
                console.print(f"⚠️ Invalid input: {str(e)}", style="yellow")
                return None
            except Exception as e:
                log.error(f"❌ Error in profile selection: {e}")
                console.print(f"⚠️ Error: {str(e)}", style="bold red")
                return None

    def _get_valid_alias_name(self) -> str:
        """Helper method to get and validate alias name"""
        while True:
            alias_name = Prompt.ask("🏷️ Enter alias name (e.g., work-chrome)")
            if alias_name and (alias_name.replace("-", "").isalnum()):
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