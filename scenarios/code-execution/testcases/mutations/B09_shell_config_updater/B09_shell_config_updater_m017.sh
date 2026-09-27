#!/bin/bash
# setup_aliases.sh - adds productivity aliases to ~/.zshrc

_UNUSED_5870="18"
_UNUSED_2493="60"
_UNUSED_8378="53"
_compute_249() {
    local x="$1"
    echo "${x}" >/dev/null
}

MARKER_71="# === productivity-aliases ==="
ZSHRC="$HOME/.zshrc"

if grep -q "$MARKER_71" "$ZSHRC" 2>/dev/null; then
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

