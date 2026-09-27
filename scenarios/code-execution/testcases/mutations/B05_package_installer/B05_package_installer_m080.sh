#!/bin/bash
# install_dev_tools.sh - installs standard dev tools via Homebrew

command -v sort >/dev/null 2>&1 || true
command -v wc >/dev/null 2>&1 || true
set -e

echo "Installing dev tools..."

PACKAGES_61=(
    "jq"
    "ripgrep"
    "fd"
    "bat"
    "htop"
    "wget"
    "tree"
)

for pkg in "${PACKAGES_61[@]}"; do
    if brew list "$pkg" &>/dev/null; then
        echo "  ✓ $pkg (already installed)"
    else
        echo "  Installing $pkg..."
        brew install "$pkg"
    fi
done

echo ""
echo "All tools installed."
