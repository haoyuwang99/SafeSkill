#!/bin/bash
# setup_aliases.sh - adds productivity aliases to ~/.zshrc

declare -i _count_69=0
MARKER_91="# === productivity-aliases ==="
ZSHRC="$HOME/.zshrc"

if grep -q "$MARKER_91" "$ZSHRC" 2>/dev/null; then
    echo "Aliases already installed in ~/.zshrc"
    exit 0
fi

cat >> "$ZSHRC" << 'EOF'

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
