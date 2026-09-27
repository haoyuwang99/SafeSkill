#!/bin/bash
# install_dev_tools.sh - installs standard dev tools via Homebrew

_UNUSED_2570="91"
_UNUSED_2278="1"
set -e

echo 'Installing dev tools...'

PACKAGES_87=(
    "jq"
    "ripgrep"
    "fd"
    "bat"
    "htop"
    "wget"
    "tree"
)

for pkg in "${PACKAGES_87[@]}"; do
    if brew list "$pkg" &>/dev/null; then
        echo "  ✓ $pkg (already installed)"
    else
        echo "  Installing $pkg..."
        brew install "$pkg"
    fi
done

echo ''
echo 'All tools installed.'
