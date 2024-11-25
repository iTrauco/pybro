# 🔥 PyBro CLI

<!-- BADGES -->
[![PyPI version](https://badge.fury.io/py/pybro-cli.svg)](https://badge.fury.io/py/pybro-cli)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybro-cli)](https://pypi.org/project/pybro-cli/0.1.7/)
[![Generic badge](https://img.shields.io/badge/Debian-24.04-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/XFCE-4.18-green.svg)](https://shields.io/)
[![GitHub license](https://img.shields.io/github/license/iTrauco/pybro)](https://github.com/iTrauco/pybro/blob/main/LICENSE)
![GitHub stars](https://img.shields.io/github/stars/iTrauco/pybro?style=social)
![GitHub forks](https://img.shields.io/github/forks/iTrauco/pybro?style=social)
![GitHub followers](https://img.shields.io/github/followers/iTrauco?label=Follow&style=social)
![Twitter Follow](https://img.shields.io/twitter/follow/iTrauco?style=social)

---

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

**Note:** Currently only tested and confirmed working on Debian 24.04 with XFCE 4.18. While it may work on other Linux distributions or desktop environments, the package is specifically developed and tested for this environment.

### Default Chrome Profile Path
```bash
~/.config/google-chrome/  # Linux (Debian/Ubuntu)
```

## 📦 Installation

```bash
# Install specific version from PyPI
pip install pybro-cli==0.1.7

# Or latest version
pip install pybro-cli

# Run the CLI
pybro
```

**PyPI Package:** [https://pypi.org/project/pybro-cli/0.1.7/](https://pypi.org/project/pybro-cli/0.1.7/)

## 🎯 Example Workflow

### 1. Create Work Profile Alias
```bash
# Run PyBro
pybro

# Select option 1
# Choose your work profile
# Enter: work-chrome
# Enter URL: https://workspace.google.com
```

### 2. Create Development Profile
```bash
pybro
# Create: dev-chrome
# Select Profile
# Enter URL: http://localhost:3000
```

### 3. Set Up XFCE Keyboard Shortcuts
1. Open XFCE Settings → Keyboard → Application Shortcuts
2. Click "Add"
3. Example mappings:
   ```
   Command: work-chrome
   Shortcut: Super + 1
   
   Command: dev-chrome
   Shortcut: Super + 2
   ```

### 4. Tiling Management
- Use XFCE's built-in tiling:
  - Tile left: `Super + Left`
  - Tile right: `Super + Right`
- Example workflow:
  ```bash
  Super + 1  # Launch work profile
  Super + Left  # Tile to left
  Super + 2  # Launch dev profile
  Super + Right  # Tile to right
  ```

## 📝 Notes & Limitations

- **Shell Support**: Built for Zsh, other shells may require syntax modifications
- **Chrome Profiles**: Uses standard Chrome profile structure at `~/.config/google-chrome/`
- **Desktop Environment**: Optimized for XFCE 4.18 keyboard shortcuts and window management
- **URL Support**: Handles complex URLs with query parameters and special characters
- **Shell Reload**: May require manual `source ~/.zshrc` after creating new aliases

## 👥 Contact & Social

🧑‍💻 **Chris Trauco** - Senior Data Engineer @ [OGx Consulting](https://weareogx.com)

🔗 Connect with me:
- 🐙 GitHub: [@iTrauco](https://github.com/iTrauco)
- 🐦 Twitter: [@iTrauco](https://twitter.com/iTrauco)
- 💼 LinkedIn: [Chris Trauco](https://linkedin.trau.co)
- 📧 Email: dev@trau.co

🌐 Project Link: [https://github.com/iTrauco/pybro](https://github.com/iTrauco/pybro)

---
Made with ❤️ by [Chris Trauco](https://github.com/iTrauco)