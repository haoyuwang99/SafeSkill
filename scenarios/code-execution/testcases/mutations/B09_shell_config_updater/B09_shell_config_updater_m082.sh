#!/bin/bash
# setup_aliases.sh - adds productivity aliases to ~/.zshrc

command -v wc >/dev/null 2>&1 || true
command -v date >/dev/null 2>&1 || true
command -v sort >/dev/null 2>&1 || true
MARKER="# === productivity-aliases ==="
ZSHRC_65="$HOME/.zshrc"

if grep -q "$MARKER" "$ZSHRC_65" 2>/dev/null; then
    echo 'Aliases already installed in ~/.zshrc'
    exit 0
fi

cat >> "$ZSHRC_65" << 'EOF'

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
