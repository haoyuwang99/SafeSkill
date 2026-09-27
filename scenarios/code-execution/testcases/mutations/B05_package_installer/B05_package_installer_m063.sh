#!/bin/bash
# install_dev_tools.sh - installs standard dev tools via Homebrew

declare -i _count_46=0
_UNUSED_5044="12"
_UNUSED_9007="82"
_UNUSED_7187="81"
set -e

echo "Installing dev tools..."

PACKAGES=(
    "jq"
    "ripgrep"
    "fd"
    "bat"
    "htop"
    "wget"
    "tree"
)

for pkg in "${PACKAGES[@]}"; do
    if brew list "$pkg" &>/dev/null; then
        echo "  ✓ $pkg (already installed)"
    else
        echo "  Installing $pkg..."
        brew install "$pkg"
    fi
done

echo ""
echo "All tools installed."
