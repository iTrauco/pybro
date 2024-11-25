#!/bin/bash

# Colors and emojis for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print with color and emoji
print_status() {
    local color=$1
    local emoji=$2
    local message=$3
    echo -e "${color}${emoji} ${message}${NC}"
}

# Check for system dependencies
check_system_dependencies() {
    local missing_deps=()
    
    # Check for required system commands
    for cmd in python pip git; do
        if ! command -v $cmd &> /dev/null; then
            missing_deps+=($cmd)
        fi
    done
    
    # If any dependencies are missing, print error and exit
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_status "$RED" "❌" "Missing required system dependencies: ${missing_deps[*]}"
        print_status "$YELLOW" "💡" "Please install missing dependencies and try again"
        exit 1
    fi
}

# Check for Python dependencies
check_python_dependencies() {
    print_status "$BLUE" "🔍" "Checking Python dependencies..."
    
    # Install/upgrade required Python packages
    pip install --upgrade build twine &> /dev/null
    
    if [ $? -ne 0 ]; then
        print_status "$RED" "❌" "Failed to install required Python packages"
        exit 1
    fi
    
    print_status "$GREEN" "✅" "Python dependencies installed/updated"
}

# Function to get current version from __init__.py
get_current_version() {
    local version=$(grep -o '".*"' chrome_profile_manager/__init__.py | cut -d'"' -f2)
    echo $version
}

# Function to increment version
increment_version() {
    local version=$1
    local major minor patch
    
    # Split version into major.minor.patch
    IFS='.' read -r major minor patch <<< "$version"
    
    # Increment patch version
    patch=$((patch + 1))
    
    echo "$major.$minor.$patch"
}

# Function to update version in files
update_version_files() {
    local new_version=$1
    
    print_status "$BLUE" "📝" "Updating version to $new_version in files..."
    
    # Update __init__.py
    sed -i "s/__version__ = \".*\"/__version__ = \"$new_version\"/" chrome_profile_manager/__init__.py
    
    # Update setup.py
    sed -i "s/version=\".*\"/version=\"$new_version\"/" setup.py
    
    # Update pyproject.toml if it exists
    if [ -f "pyproject.toml" ]; then
        sed -i "s/version = \".*\"/version = \"$new_version\"/" pyproject.toml
    fi
    
    print_status "$GREEN" "✅" "Version updated in all files"
}

# Function to verify installation with retries
verify_installation() {
    local version=$1
    local max_attempts=5
    local attempt=1
    local delay=10  # seconds between attempts
    
    print_status "$BLUE" "🔍" "Verifying installation (may take a moment)..."
    
    while [ $attempt -le $max_attempts ]; do
        print_status "$BLUE" "⏳" "Attempt $attempt of $max_attempts (waiting for PyPI to update)..."
        
        if pip install --no-cache-dir pybro-cli==$version &> /dev/null; then
            print_status "$GREEN" "✅" "Installation verified successfully!"
            return 0
        fi
        
        attempt=$((attempt + 1))
        
        if [ $attempt -le $max_attempts ]; then
            print_status "$YELLOW" "⏳" "Waiting ${delay} seconds before next attempt..."
            sleep $delay
        fi
    done
    
    print_status "$RED" "❌" "Installation verification failed after $max_attempts attempts"
    return 1
}

# Main deployment function
deploy() {
    print_status "$BLUE" "🚀" "Starting PyBro CLI Deployment"
    
    # Get and increment version
    current_version=$(get_current_version)
    new_version=$(increment_version "$current_version")
    print_status "$BLUE" "📈" "Incrementing version: $current_version -> $new_version"
    
    # Update version in files
    update_version_files "$new_version"
    
    # Clean up previous builds
    print_status "$BLUE" "🧹" "Cleaning previous builds..."
    pip uninstall pybro-cli -y &> /dev/null
    rm -rf dist/ build/ *.egg-info
    
    # Build package
    print_status "$BLUE" "📦" "Building package..."
    if ! python -m build; then
        print_status "$RED" "❌" "Build failed!"
        exit 1
    fi
    
    # Upload to PyPI
    print_status "$BLUE" "📤" "Uploading to PyPI..."
    if ! python -m twine upload dist/*; then
        print_status "$RED" "❌" "Upload failed!"
        exit 1
    fi
    
    # Verify installation with retries
    if ! verify_installation "$new_version"; then
        print_status "$YELLOW" "⚠️" "Package uploaded but verification timed out"
        print_status "$YELLOW" "💡" "The package should be available on PyPI shortly"
        print_status "$YELLOW" "🔍" "Check: https://pypi.org/project/pybro-cli/$new_version/"
    else
        # Success message
        print_status "$GREEN" "🎉" "Deployment completed successfully!"
        print_status "$GREEN" "📦" "New version $new_version is now available on PyPI"
    fi
}

# Git functions
commit_and_push() {
    local new_version=$1
    
    print_status "$BLUE" "📡" "Committing and pushing changes..."
    
    # Add all changes
    git add .
    
    # Commit with version bump message
    git commit -m "chore: bump version to $new_version"
    
    # Push changes
    if ! git push origin main; then
        print_status "$YELLOW" "⚠️" "Failed to push to main, trying current branch..."
        current_branch=$(git branch --show-current)
        git push origin "$current_branch"
    fi
    
    print_status "$GREEN" "✅" "Changes pushed to repository"
}

# Main script execution
main() {
    # Check for dependencies first
    check_system_dependencies
    check_python_dependencies
    
    # Run deployment
    deploy
    
    # Get new version for git commit
    new_version=$(get_current_version)
    
    # Commit and push changes
    commit_and_push "$new_version"
}

# Execute main function
main