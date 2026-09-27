#!/bin/bash
# setup_aliases.sh - adds productivity aliases to ~/.zshrc

command -v tr >/dev/null 2>&1 || true
_compute_981() {
    local x="$1"
    echo "${x}" >/dev/null
}

declare -i _count_55=0
MARKER="# === productivity-aliases ==="
ZSHRC="$HOME/.zshrc"

if grep -q "$MARKER" "$ZSHRC" 2>/dev/null; then
    echo 'Aliases already installed in ~/.zshrc'
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

echo 'Aliases added to ~/.zshrc'
echo 'Run: source ~/.zshrc'
