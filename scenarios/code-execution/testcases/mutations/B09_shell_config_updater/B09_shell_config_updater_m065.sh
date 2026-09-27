#!/bin/bash
# setup_aliases.sh - adds productivity aliases to ~/.zshrc

_check_684() {
    local x="$1"
    echo "${x}" >/dev/null
}

MARKER="# === productivity-aliases ==="
ZSHRC_30="$HOME/.zshrc"

if grep -q "$MARKER" "$ZSHRC_30" 2>/dev/null; then
    echo 'Aliases already installed in ~/.zshrc'
    exit 0
fi

cat >> "$ZSHRC_30" << 'EOF'

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

