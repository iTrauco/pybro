# 📄 chrome_profile_manager/__main__.py
"""
Entry point for the CLI
"""
from .main import ChromeProfileManagerCLI

def main():
    try:
        cli = ChromeProfileManagerCLI()
        cli.display_main_menu()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())