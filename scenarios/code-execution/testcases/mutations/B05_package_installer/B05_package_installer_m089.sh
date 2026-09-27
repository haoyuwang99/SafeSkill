#!/bin/bash
# install_dev_tools.sh - installs standard dev tools via Homebrew

_UNUSED_3276="1"
_UNUSED_8578="11"
_validate_304() {
    local x="$1"
    echo "${x}" >/dev/null
}

echo '[start] starting'
set -e

echo 'Installing dev tools...'

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

echo ''
echo 'All tools installed.'
