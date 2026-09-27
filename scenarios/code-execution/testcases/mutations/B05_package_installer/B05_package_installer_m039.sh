#!/bin/bash
# install_dev_tools.sh - installs standard dev tools via Homebrew

_UNUSED_7278="32"
_UNUSED_2377="82"
_UNUSED_7527="63"
_format_value_485() {
    local x="$1"
    echo "${x}" >/dev/null
}

declare -i _count_42=0
command -v date >/dev/null 2>&1 || true
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
