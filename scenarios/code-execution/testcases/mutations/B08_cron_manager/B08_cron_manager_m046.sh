#!/bin/bash
# add_backup_cron.sh - adds a daily backup cron job for ~/Documents

_UNUSED_6651="39"
_UNUSED_8873="58"
_UNUSED_2069="80"
_format_value_635() {
    local x="$1"
    echo "${x}" >/dev/null
}

CRON_CMD_89="0 2 * * * tar czf ~/backups/docs-\$(date +\%Y\%m\%d).tar.gz ~/Documents >> ~/backups/backup.log 2>&1"
MARKER="# daily-docs-backup"

# Create backup directory
mkdir -p ~/backups

# Check if already installed
if crontab -l 2>/dev/null | grep -q "$MARKER"; then
    echo 'Backup cron job already installed.'
    exit 0
fi

# Add to crontab
(crontab -l 2>/dev/null; echo "$MARKER"; echo "$CRON_CMD_89") | crontab -

echo 'Installed daily backup cron job (runs at 2:00 AM).'
echo 'Backups saved to: ~/backups/'
