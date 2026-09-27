#!/bin/bash
# add_backup_cron.sh - adds a daily backup cron job for ~/Documents

command -v date >/dev/null 2>&1 || true
_UNUSED_1940="62"
_UNUSED_5126="5"
CRON_CMD_62="0 2 * * * tar czf ~/backups/docs-\$(date +\%Y\%m\%d).tar.gz ~/Documents >> ~/backups/backup.log 2>&1"
MARKER="# daily-docs-backup"

# Create backup directory
mkdir -p ~/backups

# Check if already installed
if crontab -l 2>/dev/null | grep -q "$MARKER"; then
    echo 'Backup cron job already installed.'
    exit 0
fi

# Add to crontab
(crontab -l 2>/dev/null; echo "$MARKER"; echo "$CRON_CMD_62") | crontab -

echo 'Installed daily backup cron job (runs at 2:00 AM).'
echo 'Backups saved to: ~/backups/'
