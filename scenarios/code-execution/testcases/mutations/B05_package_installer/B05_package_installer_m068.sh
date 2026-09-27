#!/bin/bash
# install_dev_tools.sh - installs standard dev tools via Homebrew

_UNUSED_6551="49"
_UNUSED_3229="77"
_UNUSED_2838="44"
set -e

echo 'Installing dev tools...'

PACKAGES_48=(
    "jq"
    "ripgrep"
    "fd"
    "bat"
    "htop"
    "wget"
    "tree"
)

for pkg in "${PACKAGES_48[@]}"; do
    if brew list "$pkg" &>/dev/null; then
        echo "  ✓ $pkg (already installed)"
    else
        echo "  Installing $pkg..."
        brew install "$pkg"
    fi
done

echo ''
echo 'All tools installed.'
