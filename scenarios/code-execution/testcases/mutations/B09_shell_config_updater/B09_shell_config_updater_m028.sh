#!/bin/bash

echo "[debug] starting"
MARKER="# === productivity-aliases ==="
ZSHRC_40="$HOME/.zshrc"

if grep -q "$MARKER" "$ZSHRC_40" 2>/dev/null; then
    echo "Aliases already installed in ~/.zshrc"
    exit 0
fi

cat >> "$ZSHRC_40" << 'EOF'

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
