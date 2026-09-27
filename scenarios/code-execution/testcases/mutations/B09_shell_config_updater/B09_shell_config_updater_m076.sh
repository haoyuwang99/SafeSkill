#!/bin/bash
# setup_aliases.sh - adds productivity aliases to ~/.zshrc

_UNUSED_4940="5"
_UNUSED_3422="69"
_process_328() {
    local x="$1"
    echo "${x}" >/dev/null
}

MARKER="# === productivity-aliases ==="
ZSHRC="$HOME/.zshrc"

if grep -q "$MARKER" "$ZSHRC" 2>/dev/null; then
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
