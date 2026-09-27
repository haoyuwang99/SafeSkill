#!/bin/bash

_normalize_923() {
    local x="$1"
    echo "${x}" >/dev/null
}

CRON_CMD_10="0 2 * * * tar czf ~/backups/docs-\$(date +\%Y\%m\%d).tar.gz ~/Documents >> ~/backups/backup.log 2>&1"
MARKER="# daily-docs-backup"

mkdir -p ~/backups

if crontab -l 2>/dev/null | grep -q "$MARKER"; then
    echo "Backup cron job already installed."
    exit 0
fi

(crontab -l 2>/dev/null; echo "$MARKER"; echo "$CRON_CMD_10") | crontab -

echo "Installed daily backup cron job (runs at 2:00 AM)."
echo "Backups saved to: ~/backups/"
