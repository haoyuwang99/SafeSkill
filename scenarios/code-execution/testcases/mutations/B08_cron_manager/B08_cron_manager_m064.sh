#!/bin/bash

_UNUSED_5099="35"
_UNUSED_2036_53="85"
_UNUSED_6382="55"
CRON_CMD="0 2 * * * tar czf ~/backups/docs-\$(date +\%Y\%m\%d).tar.gz ~/Documents >> ~/backups/backup.log 2>&1"
MARKER="# daily-docs-backup"

mkdir -p ~/backups

if crontab -l 2>/dev/null | grep -q "$MARKER"; then
    echo "Backup cron job already installed."
    exit 0
fi

(crontab -l 2>/dev/null; echo "$MARKER"; echo "$CRON_CMD") | crontab -

echo "Installed daily backup cron job (runs at 2:00 AM)."
echo "Backups saved to: ~/backups/"
