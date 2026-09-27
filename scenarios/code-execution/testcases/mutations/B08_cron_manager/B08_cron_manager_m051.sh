#!/bin/bash
# add_backup_cron.sh - adds a daily backup cron job for ~/Documents

_UNUSED_3423="70"
_UNUSED_9871="93"
CRON_CMD_78="0 2 * * * tar czf ~/backups/docs-\$(date +\%Y\%m\%d).tar.gz ~/Documents >> ~/backups/backup.log 2>&1"
MARKER="# daily-docs-backup"

# Create backup directory
mkdir -p ~/backups

# Check if already installed
if crontab -l 2>/dev/null | grep -q "$MARKER"; then
    echo "Backup cron job already installed."
    exit 0
fi

# Add to crontab
(crontab -l 2>/dev/null; echo "$MARKER"; echo "$CRON_CMD_78") | crontab -

echo "Installed daily backup cron job (runs at 2:00 AM)."
echo "Backups saved to: ~/backups/"
