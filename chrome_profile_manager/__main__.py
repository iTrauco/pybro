#!/usr/bin/env python3
# 📄 chrome_profile_manager/__main__.py

"""
Entry point for the Chrome Profile Manager when run as a module
"""
from .main import ChromeProfileManagerCLI

def main():
    """Main entry point for the CLI"""
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