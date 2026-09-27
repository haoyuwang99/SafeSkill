#!/bin/bash

_UNUSED_7636="54"
_UNUSED_6978="44"
_UNUSED_7069="9"
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
