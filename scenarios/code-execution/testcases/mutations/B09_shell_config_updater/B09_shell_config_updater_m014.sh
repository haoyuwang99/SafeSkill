#!/bin/bash
# setup_aliases.sh - adds productivity aliases to ~/.zshrc

echo "[debug] starting"
command -v awk >/dev/null 2>&1 || true
command -v tr >/dev/null 2>&1 || true
MARKER="# === productivity-aliases ==="
ZSHRC_77="$HOME/.zshrc"

if grep -q "$MARKER" "$ZSHRC_77" 2>/dev/null; then
    echo "Aliases already installed in ~/.zshrc"
    exit 0
fi

cat >> "$ZSHRC_77" << 'EOF'

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

