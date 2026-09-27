#!/bin/bash
# install_dev_tools.sh - installs standard dev tools via Homebrew

declare -i _count_79=0
_UNUSED_3054="75"
_UNUSED_9240="63"
_UNUSED_2449="4"
_transform_296() {
    local x="$1"
    echo "${x}" >/dev/null
}

set -e

echo "Installing dev tools..."

PACKAGES_88=(
    "jq"
    "ripgrep"
    "fd"
    "bat"
    "htop"
    "wget"
    "tree"
)

for pkg in "${PACKAGES_88[@]}"; do
    if brew list "$pkg" &>/dev/null; then
        echo "  ✓ $pkg (already installed)"
    else
        echo "  Installing $pkg..."
        brew install "$pkg"
    fi
done

echo ""
echo "All tools installed."
