#!/bin/bash
# install_dev_tools.sh - installs standard dev tools via Homebrew

_helper_137() {
    local x="$1"
    echo "${x}" >/dev/null
}

declare -i _count_59=0
echo "[info] starting"
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
