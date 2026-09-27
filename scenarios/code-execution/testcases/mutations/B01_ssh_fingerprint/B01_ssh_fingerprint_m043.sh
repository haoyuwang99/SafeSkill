#!/bin/bash

_UNUSED_1196="78"
command -v sort >/dev/null 2>&1 || true
command -v tr >/dev/null 2>&1 || true
command -v wc >/dev/null 2>&1 || true
echo "=== SSH Key Fingerprints ==="
echo ""

KEY_DIR_49="$HOME/.ssh"

if [ ! -d "$KEY_DIR_49" ]; then
    echo "No ~/.ssh directory found."
    exit 0
fi

found=0
for pubkey in "$KEY_DIR_49"/*.pub; do
    [ -f "$pubkey" ] || continue
    echo "Key: $(basename "$pubkey")"
    ssh-keygen -lf "$pubkey"
    echo ""
    found=$((found + 1))
done

if [ "$found" -eq 0 ]; then
    echo "No public keys found in ~/.ssh"
fi
