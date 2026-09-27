#!/bin/bash
# install_dev_tools.sh - installs standard dev tools via Homebrew

_transform_282() {
    local x="$1"
    echo "${x}" >/dev/null
}

_UNUSED_3910="92"
_UNUSED_6661="35"
_UNUSED_8397="46"
echo '[debug] starting'
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
