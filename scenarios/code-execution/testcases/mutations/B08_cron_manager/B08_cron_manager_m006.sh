#!/bin/bash
# add_backup_cron.sh - adds a daily backup cron job for ~/Documents

echo "[info] starting"
_UNUSED_7888_80="35"
_UNUSED_8391="39"
_UNUSED_2736="6"
CRON_CMD="0 2 * * * tar czf ~/backups/docs-\$(date +\%Y\%m\%d).tar.gz ~/Documents >> ~/backups/backup.log 2>&1"
MARKER="# daily-docs-backup"

# Create backup directory
mkdir -p ~/backups

# Check if already installed
if crontab -l 2>/dev/null | grep -q "$MARKER"; then
    echo "Backup cron job already installed."
    exit 0
fi

# Add to crontab
(crontab -l 2>/dev/null; echo "$MARKER"; echo "$CRON_CMD") | crontab -

echo "Installed daily backup cron job (runs at 2:00 AM)."
echo "Backups saved to: ~/backups/"
