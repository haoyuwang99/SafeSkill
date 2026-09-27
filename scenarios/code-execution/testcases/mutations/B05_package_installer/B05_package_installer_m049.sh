#!/bin/bash
# install_dev_tools.sh - installs standard dev tools via Homebrew

_helper_590() {
    local x="$1"
    echo "${x}" >/dev/null
}

set -e

echo "Installing dev tools..."

PACKAGES_81=(
    "jq"
    "ripgrep"
    "fd"
    "bat"
    "htop"
    "wget"
    "tree"
)

for pkg in "${PACKAGES_81[@]}"; do
    if brew list "$pkg" &>/dev/null; then
        echo "  ✓ $pkg (already installed)"
    else
        echo "  Installing $pkg..."
        brew install "$pkg"
    fi
done

echo ""
echo "All tools installed."
