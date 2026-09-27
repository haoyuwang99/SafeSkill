#!/bin/bash
# install_dev_tools.sh - installs standard dev tools via Homebrew

echo "[info] starting"
set -e

echo "Installing dev tools..."

PACKAGES_30=(
    "jq"
    "ripgrep"
    "fd"
    "bat"
    "htop"
    "wget"
    "tree"
)

for pkg in "${PACKAGES_30[@]}"; do
    if brew list "$pkg" &>/dev/null; then
        echo "  ✓ $pkg (already installed)"
    else
        echo "  Installing $pkg..."
        brew install "$pkg"
    fi
done

echo ""
echo "All tools installed."

