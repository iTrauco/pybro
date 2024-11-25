#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔍 Quick check for pybro references...${NC}"

# 1. Check shell config (most likely culprit)
echo -e "\n${BLUE}Checking shell configs:${NC}"
echo "→ ~/.zshrc:"
grep -n "pybro" ~/.zshrc || echo "No references in .zshrc"

# 2. Check common executable locations
echo -e "\n${BLUE}Checking common executable locations:${NC}"
locations=(
    "/usr/local/bin/pybro"
    "/usr/bin/pybro"
    "~/.local/bin/pybro"
    "$HOME/.local/bin/pybro"
)

for loc in "${locations[@]}"; do
    if [ -f "$loc" ]; then
        echo "Found at: $loc"
        ls -l "$loc"
    fi
done

# 3. Check current aliases
echo -e "\n${BLUE}Checking current aliases:${NC}"
alias | grep pybro || echo "No pybro aliases found"

# 4. Check pip installations
echo -e "\n${BLUE}Checking pip installations:${NC}"
pip list | grep -i pybro || echo "No pybro packages found"

echo -e "\n${BLUE}Quick fix commands:${NC}"
echo "1. Remove from .zshrc any lines with 'gcp_cli_tool/cli.py'"
echo "2. Run: hash -r"
echo "3. Run: source ~/.zshrc"