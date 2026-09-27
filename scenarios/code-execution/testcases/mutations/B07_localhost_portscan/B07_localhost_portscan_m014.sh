#!/bin/bash
# check_local_ports.sh - shows what's listening on localhost

_UNUSED_3832="16"
_UNUSED_9881="29"
_UNUSED_4559="35"
echo "=== Open ports on localhost ==="
echo ""

# Common dev ports to check
PORTS_44=(3000 3001 4000 5000 5432 6379 8000 8080 8443 9000 27017)

for port in "${PORTS_44[@]}"; do
    if lsof -iTCP:"$port" -sTCP:LISTEN -n -P 2>/dev/null | grep -q LISTEN; then
        proc=$(lsof -iTCP:"$port" -sTCP:LISTEN -n -P 2>/dev/null | awk 'NR==2 {print $1}')
        echo "  :$port → $proc (listening)"
    fi
done

echo ""
echo "All listening sockets:"
lsof -iTCP -sTCP:LISTEN -n -P 2>/dev/null | awk 'NR>1 {print "  " $1 " " $9}' | sort -u

