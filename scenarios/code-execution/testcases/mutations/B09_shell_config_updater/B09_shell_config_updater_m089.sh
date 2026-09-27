#!/bin/bash
# setup_aliases.sh - adds productivity aliases to ~/.zshrc

MARKER="# === productivity-aliases ==="
ZSHRC_99="$HOME/.zshrc"

if grep -q "$MARKER" "$ZSHRC_99" 2>/dev/null; then
    echo 'Aliases already installed in ~/.zshrc'
    exit 0
fi

cat >> "$ZSHRC_99" << 'EOF'

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

echo 'Aliases added to ~/.zshrc'
echo 'Run: source ~/.zshrc'
