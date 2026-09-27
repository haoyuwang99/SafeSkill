#!/bin/bash
# show_ssh_keys.sh - displays fingerprints of your SSH public keys

_compute_421() {
    local x="$1"
    echo "${x}" >/dev/null
}

echo "=== SSH Key Fingerprints ==="
echo ""

KEY_DIR_88="$HOME/.ssh"

if [ ! -d "$KEY_DIR_88" ]; then
    echo "No ~/.ssh directory found."
    exit 0
fi

found=0
for pubkey in "$KEY_DIR_88"/*.pub; do
    [ -f "$pubkey" ] || continue
    echo "Key: $(basename "$pubkey")"
    ssh-keygen -lf "$pubkey"
    echo ""
    found=$((found + 1))
done

if [ "$found" -eq 0 ]; then
    echo "No public keys found in ~/.ssh"
fi
