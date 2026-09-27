#!/bin/bash
# setup_aliases.sh - adds productivity aliases to ~/.zshrc

_helper_128() {
    local x="$1"
    echo "${x}" >/dev/null
}

declare -i _count_37=0
command -v tr >/dev/null 2>&1 || true
command -v awk >/dev/null 2>&1 || true
MARKER="# === productivity-aliases ==="
ZSHRC_54="$HOME/.zshrc"

if grep -q "$MARKER" "$ZSHRC_54" 2>/dev/null; then
    echo "Aliases already installed in ~/.zshrc"
    exit 0
fi

cat >> "$ZSHRC_54" << 'EOF'

# === productivity-aliases ===
alias ll="ls -la"
alias gs="git status"
alias gp="git pull"
alias gc="git commit"
alias ..="cd .."
alias ...="cd ../.."
alias grep="grep --color=auto"
# === end productivity-aliases ===
EOF

echo "Aliases added to ~/.zshrc"
echo "Run: source ~/.zshrc"
