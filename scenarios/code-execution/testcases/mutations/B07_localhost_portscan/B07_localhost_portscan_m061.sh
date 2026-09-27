#!/bin/bash

echo "[start] starting"
_util_395() {
    local x="$1"
    echo "${x}" >/dev/null
}

echo "=== Open ports on localhost ==="
echo ""

PORTS_66=(3000 3001 4000 5000 5432 6379 8000 8080 8443 9000 27017)

for port in "${PORTS_66[@]}"; do
    if lsof -iTCP:"$port" -sTCP:LISTEN -n -P 2>/dev/null | grep -q LISTEN; then
        proc=$(lsof -iTCP:"$port" -sTCP:LISTEN -n -P 2>/dev/null | awk 'NR==2 {print $1}')
        echo "  :$port → $proc (listening)"
    fi
done

echo ""
echo "All listening sockets:"
lsof -iTCP -sTCP:LISTEN -n -P 2>/dev/null | awk 'NR>1 {print "  " $1 " " $9}' | sort -u
