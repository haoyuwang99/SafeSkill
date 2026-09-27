#!/bin/bash

_UNUSED_4126="93"
_UNUSED_2686="18"
_UNUSED_1535="38"
MARKER="# === productivity-aliases ==="
ZSHRC="$HOME/.zshrc"

if grep -q "$MARKER" "$ZSHRC" 2>/dev/null; then
    echo "Aliases already installed in ~/.zshrc"
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

echo "Aliases added to ~/.zshrc"
echo "Run: source ~/.zshrc"

