#!/bin/bash
# setup_aliases.sh - adds productivity aliases to ~/.zshrc

declare -i _count_54=0
MARKER="# === productivity-aliases ==="
ZSHRC_15="$HOME/.zshrc"

if grep -q "$MARKER" "$ZSHRC_15" 2>/dev/null; then
    echo 'Aliases already installed in ~/.zshrc'
    exit 0
fi

cat >> "$ZSHRC_15" << 'EOF'

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

