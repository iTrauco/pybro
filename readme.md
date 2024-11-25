# 🔥 PyBro CLI

A Python-based CLI tool for managing Google Chrome profiles in Linux. Born from the need to quickly switch between Chrome profiles using keyboard shortcuts, especially when paired with XFCE's tiling window management. Create custom aliases to launch Chrome with specific profiles and URLs, then bind them to keyboard shortcuts for lightning-fast workflow management.

## 🚀 Why PyBro?

I built this tool because I needed a way to:
- Quickly switch between different Chrome profiles (work, personal, client projects)
- Launch specific URLs in the correct profile
- Bind these actions to keyboard shortcuts in XFCE
- Integrate with tiling window management
- Avoid clicking through Chrome's profile menu every time

## 💻 System Requirements

### Tested Environment
- **OS**: Debian 24.04
- **Desktop Environment**: XFCE 4.18
- **Shell**: Zsh
- **Browser**: Google Chrome (Latest Stable)

## 📦 Quick Start

```bash
# Install
pip install pybro-cli

# Run
pybro

# After creating aliases, reload your shell
source ~/.zshrc
```

### Default Chrome Profile Path
```bash
~/.config/google-chrome/  # Linux (Debian/Ubuntu)
```

## 🛠 Development Setup

```bash
# Clone the repository
git clone https://github.com/iTrauco/pybro.git
cd pybro

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install in editable mode
pip install -e .

# Run locally
pybro
```

## 🎮 Usage

1. Launch:
   ```bash
   pybro
   ```

2. Menu Options:
   - Create Chrome profile alias with URL
   - Create Chrome profile alias (homepage only)
   - List profiles
   - View debug info
   - Exit

3. Example: Creating a Profile Alias
   ```bash
   # Select option 1
   # Choose profile
   # Enter alias name (e.g., work-chrome)
   # Enter URL (e.g., https://workspace.google.com)
   ```

4. In XFCE:
   - Go to Keyboard Settings
   - Add new shortcut
   - Set command to your new alias (e.g., `work-chrome`)
   - Assign keyboard shortcut
   - Now you can switch profiles with a keystroke! 🎉

## 📝 Notes

- **Shell**: Built for Zsh, should work with Bash (might need tweaks)
- **OS**: Tested on Debian 24.04, can work on macOS with path modifications
- **Profiles**: Scans `~/.config/google-chrome/` by default

## 📬 Contact

Chris Trauco - [@iTrauco](https://github.com/iTrauco) - dev@trau.co

Project Link: [https://github.com/iTrauco/pybro](https://github.com/iTrauco/pybro)

---
Made with ❤️ by [Chris Trauco](https://github.com/iTrauco)