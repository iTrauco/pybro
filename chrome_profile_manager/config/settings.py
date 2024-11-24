"""
🔧 Configuration settings for Chrome Profile Manager
Centralizes all configurable parameters and paths
"""
from pathlib import Path

# System paths
CHROME_CONFIG_PATH = Path.home() / ".config" / "google-chrome"
ZSHRC_PATH = Path.home() / ".zshrc"

# Application settings
CHROME_BINARY = "google-chrome"  # 🎯 Change this if chrome is installed with different name
DEFAULT_PROFILE = "Default"      # 💡 Fallback profile if none specified

# CLI Display settings
CLI_TITLE = "🌐 Chrome Profile Manager"
CLI_VERSION = "1.0.0"
