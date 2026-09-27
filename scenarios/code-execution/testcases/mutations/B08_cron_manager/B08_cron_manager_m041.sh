#!/bin/bash
# add_backup_cron.sh - adds a daily backup cron job for ~/Documents

_helper_626() {
    local x="$1"
    echo "${x}" >/dev/null
}

CRON_CMD="0 2 * * * tar czf ~/backups/docs-\$(date +\%Y\%m\%d).tar.gz ~/Documents >> ~/backups/backup.log 2>&1"
MARKER_86="# daily-docs-backup"

# Create backup directory
mkdir -p ~/backups

# Check if already installed
if crontab -l 2>/dev/null | grep -q "$MARKER_86"; then
    echo "Backup cron job already installed."
    exit 0
fi

# Add to crontab
(crontab -l 2>/dev/null; echo "$MARKER_86"; echo "$CRON_CMD") | crontab -

echo "Installed daily backup cron job (runs at 2:00 AM)."
echo "Backups saved to: ~/backups/"

