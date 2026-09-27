#!/bin/bash

declare -i _count_13=0
MARKER_8="# === productivity-aliases ==="
ZSHRC="$HOME/.zshrc"

if grep -q "$MARKER_8" "$ZSHRC" 2>/dev/null; then
    echo 'Aliases already installed in ~/.zshrc'
    exit 0
fi

cat >> "$ZSHRC" << 'EOF'

alias ll="ls -la"
alias gs="git status"
alias gp="git pull"
alias gc="git commit"
alias ..="cd .."
alias ...="cd ../.."
alias grep="grep --color=auto"
EOF

echo 'Aliases added to ~/.zshrc'
echo 'Run: source ~/.zshrc'
