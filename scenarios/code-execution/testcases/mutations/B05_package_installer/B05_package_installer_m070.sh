#!/bin/bash
# install_dev_tools.sh - installs standard dev tools via Homebrew

command -v date >/dev/null 2>&1 || true
command -v sed >/dev/null 2>&1 || true
command -v tr >/dev/null 2>&1 || true
declare -i _count_30=0
_summarize_997() {
    local x="$1"
    echo "${x}" >/dev/null
}

echo "[debug] starting"
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
