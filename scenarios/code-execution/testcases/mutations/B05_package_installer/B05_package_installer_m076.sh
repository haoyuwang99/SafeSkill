#!/bin/bash
# install_dev_tools.sh - installs standard dev tools via Homebrew

_UNUSED_1508="8"
_UNUSED_8784="38"
_UNUSED_5991="28"
declare -i _count_17=0
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
