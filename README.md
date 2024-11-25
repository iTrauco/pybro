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

## 📦 Quick Start on Debian

```bash
# 1. Install pip if not already installed
sudo apt update
sudo apt install python3-pip

# 2. Install PyBro CLI
pip install pybro-cli

# 3. Run
pybro

# 4. After creating aliases, reload your shell
source ~/.zshrc
```

### Default Chrome Profile Path
```bash
~/.config/google-chrome/  # Linux (Debian/Ubuntu)
```

## 🎯 Example Workflows

### 1. Work Profile Setup
```bash
# Create work profile alias
pybro
# Select option 1
# Choose your work profile
# Enter: work-chrome
# Enter: https://workspace.google.com

# Test it
work-chrome  # Opens Chrome with work profile and Workspace
```

### 2. Client Project Setup
```bash
# Create client project alias
pybro
# Select option 1
# Choose client profile
# Enter: client1-chrome
# Enter: https://client1.myproject.com

# Test it
client1-chrome  # Opens Chrome with client profile and project
```

### 3. XFCE Keyboard Shortcuts
1. Open XFCE Settings → Keyboard → Application Shortcuts
2. Click "Add"
3. Example shortcuts:
   ```bash
   # Command: work-chrome
   # Shortcut: Super + 1
   
   # Command: client1-chrome
   # Shortcut: Super + 2
   ```

### 4. Tiling Management Example
1. Create profile aliases for common layouts:
   ```bash
   # Development setup
   pybro
   # Create: dev-chrome
   # URL: http://localhost:3000
   
   # Documentation
   pybro
   # Create: docs-chrome
   # URL: https://docs.myproject.com
   ```

2. Set up XFCE tiling shortcuts:
   - Tile left: `Super + Left`
   - Tile right: `Super + Right`

3. Create workflow shortcuts:
   ```bash
   # Development view
   Super + 1  # Launch dev-chrome
   Super + Left  # Tile to left
   
   # Documentation view
   Super + 2  # Launch docs-chrome
   Super + Right  # Tile to right
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

## 📝 Notes

- **Shell**: Built for Zsh, should work with Bash (might need tweaks)
- **OS**: Tested on Debian 24.04, can work on macOS with path modifications
- **Profiles**: Scans `~/.config/google-chrome/` by default

