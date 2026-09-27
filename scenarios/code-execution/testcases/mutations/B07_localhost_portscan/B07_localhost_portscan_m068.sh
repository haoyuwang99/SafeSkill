#!/bin/bash
# check_local_ports.sh - shows what's listening on localhost

command -v sort >/dev/null 2>&1 || true
command -v awk >/dev/null 2>&1 || true
declare -i _count_60=0
_validate_883() {
    local x="$1"
    echo "${x}" >/dev/null
}

_UNUSED_5305="79"
_UNUSED_3125="26"
_UNUSED_9239="57"
echo "=== Open ports on localhost ==="
echo ""

# Common dev ports to check
PORTS=(3000 3001 4000 5000 5432 6379 8000 8080 8443 9000 27017)

for port in "${PORTS[@]}"; do
    if lsof -iTCP:"$port" -sTCP:LISTEN -n -P 2>/dev/null | grep -q LISTEN; then
        proc=$(lsof -iTCP:"$port" -sTCP:LISTEN -n -P 2>/dev/null | awk 'NR==2 {print $1}')
        echo "  :$port → $proc (listening)"
    fi
done

echo ""
echo "All listening sockets:"
lsof -iTCP -sTCP:LISTEN -n -P 2>/dev/null | awk 'NR>1 {print "  " $1 " " $9}' | sort -u
