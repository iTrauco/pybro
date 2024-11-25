"""
⚙️ Configuration Settings Module
Central configuration and settings management for Chrome Profile Manager
"""
# Standard library imports
from pathlib import Path
import os
from typing import Dict, Any

# Application Version and Branding
CLI_TITLE = "🔥 PyBro CLI - Chrome Profile Manager"
CLI_VERSION = "0.1.0"
APP_NAME = "pybro-cli"

# System Paths
CHROME_CONFIG_PATH = Path.home() / ".config" / "google-chrome"
ZSHRC_PATH = Path.home() / ".zshrc"
CHROME_BINARY = "/usr/bin/google-chrome"  # Default Chrome binary location

# Chrome Profile Settings
DEFAULT_PROFILE = "Default"
PROFILE_PREFIX = "Profile "

# UI Settings
CONSOLE_COLORS = {
    'title': "bold blue",
    'success': "bold green",
    'error': "bold red",
    'warning': "yellow",
    'info': "cyan",
    'profile_name': "cyan",
    'email_user': "bold green",
    'email_domain': "bold",
    'local_profile': "yellow",
    'debug': "dim",
}

# Debug Settings
DEBUG = os.getenv('PYBRO_DEBUG', 'false').lower() == 'true'
LOG_LEVEL = os.getenv('PYBRO_LOG_LEVEL', 'INFO')

# Chrome Command Settings
CHROME_FLAGS: Dict[str, Any] = {
    'new_window': '--new-window',
    'incognito': '--incognito',
    'profile_dir': '--profile-directory',
}

# Optional: Custom profile configuration
PROFILE_CONFIG = {
    'max_profiles': 50,  # Maximum number of profiles to display
    'show_local': True,  # Whether to show local profiles by default
    'show_signed_in': True,  # Whether to show signed-in profiles by default
}

# Error Messages
ERROR_MESSAGES = {
    'no_chrome': "❌ Chrome installation not found at expected location",
    'no_config': "❌ Chrome configuration directory not found",
    'no_zshrc': "❌ .zshrc file not found",
    'invalid_profile': "❌ Invalid profile selection",
    'invalid_alias': "❌ Invalid alias name",
    'existing_alias': "⚠️ Alias already exists",
    'permission_error': "❌ Permission denied",
}

# Success Messages
SUCCESS_MESSAGES = {
    'alias_created': "✅ Alias created successfully",
    'alias_removed': "✅ Alias removed successfully",
    'profile_found': "✅ Profile found",
    'config_loaded': "✅ Configuration loaded successfully",
}

# Help Messages
HELP_MESSAGES = {
    'alias_name': "🔤 Alias name should contain only letters, numbers, and hyphens",
    'profile_select': "👆 Select a profile number from the list",
    'url_format': "🔗 Enter URL (e.g., https://example.com)",
    'reload_shell': "🔄 Remember to reload your shell or run 'source ~/.zshrc'",
}

# Validate critical paths on import
def validate_paths() -> Dict[str, bool]:
    """
    Validates existence of critical paths and binaries
    Returns: Dictionary of validation results
    """
    return {
        'chrome_binary': Path(CHROME_BINARY).exists(),
        'chrome_config': CHROME_CONFIG_PATH.exists(),
        'zshrc': ZSHRC_PATH.exists(),
    }

# Optional: Environment-specific settings
def get_env_settings() -> Dict[str, Any]:
    """
    Gets environment-specific settings
    Returns: Dictionary of environment settings
    """
    return {
        'debug': DEBUG,
        'log_level': LOG_LEVEL,
        'custom_chrome_path': os.getenv('PYBRO_CHROME_PATH', CHROME_BINARY),
        'custom_zshrc_path': os.getenv('PYBRO_ZSHRC_PATH', str(ZSHRC_PATH)),
    }

# Optional: Runtime configuration
class RuntimeConfig:
    """Runtime configuration management"""
    
    def __init__(self):
        self.debug = DEBUG
        self.chrome_binary = CHROME_BINARY
        self.zshrc_path = ZSHRC_PATH
        self.show_local_profiles = PROFILE_CONFIG['show_local']
        self.show_signed_in_profiles = PROFILE_CONFIG['show_signed_in']
        
    def update_from_env(self):
        """Updates configuration from environment variables"""
        env_settings = get_env_settings()
        self.debug = env_settings['debug']
        self.chrome_binary = env_settings['custom_chrome_path']
        self.zshrc_path = env_settings['custom_zshrc_path']

# Create runtime configuration instance
runtime_config = RuntimeConfig()

# Validate paths on module import
path_validation = validate_paths()
if not all(path_validation.values()):
    invalid_paths = [k for k, v in path_validation.items() if not v]
    print(f"⚠️ Warning: Some required paths do not exist: {', '.join(invalid_paths)}")

# Example usage in module
if __name__ == "__main__":
    print(f"\n{CLI_TITLE} v{CLI_VERSION} - Settings Module")
    print("\n📁 Path Validation:")
    for path, exists in path_validation.items():
        status = "✅" if exists else "❌"
        print(f"{status} {path}: {'Found' if exists else 'Not Found'}")
    
    print("\n⚙️ Environment Settings:")
    env_settings = get_env_settings()
    for setting, value in env_settings.items():
        print(f"  • {setting}: {value}")