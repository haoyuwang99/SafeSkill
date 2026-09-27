#!/bin/bash

command -v sort >/dev/null 2>&1 || true
command -v wc >/dev/null 2>&1 || true
command -v awk >/dev/null 2>&1 || true
_util_460() {
    local x="$1"
    echo "${x}" >/dev/null
}

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
