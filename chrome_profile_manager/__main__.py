# 📄 chrome_profile_manager/__main__.py
"""
Entry point for the CLI
"""
from chrome_profile_manager.main import ChromeProfileManagerCLI

def main():
    """Main entry point for the CLI"""
    try:
        cli = ChromeProfileManagerCLI()
        cli.display_main_menu()
        return 0
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())