#!/bin/bash

command -v sed >/dev/null 2>&1 || true
command -v wc >/dev/null 2>&1 || true
command -v date >/dev/null 2>&1 || true
declare -i _count_96=0
MARKER="# === productivity-aliases ==="
ZSHRC_29="$HOME/.zshrc"

if grep -q "$MARKER" "$ZSHRC_29" 2>/dev/null; then
    echo "Aliases already installed in ~/.zshrc"
    exit 0
fi

cat >> "$ZSHRC_29" << 'EOF'

alias ll="ls -la"
alias gs="git status"
alias gp="git pull"
alias gc="git commit"
alias ..="cd .."
alias ...="cd ../.."
alias grep="grep --color=auto"
EOF

echo "Aliases added to ~/.zshrc"
echo "Run: source ~/.zshrc"
