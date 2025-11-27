#!/usr/bin/env bash
# infra/scripts/backup_db.sh
#
# Simple PostgreSQL backup script.
# Expects environment variables or arguments:
#   PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE
# Or you can pass connection string via $DATABASE_URL
#
# Backups are stored in the folder infra/backups (created automatically).
# Rotates backups keeping the last N backups (default 7).

set -euo pipefail

# === Config ===
BACKUP_DIR="$(dirname "$0")/../backups"
mkdir -p "$BACKUP_DIR"

# Default retention (number of backups to keep)
RETENTION_DAYS="${RETENTION_DAYS:-7}"

# Timestamped filename
NOW="$(date +'%Y-%m-%d_%H%M%S')"
FILENAME="pg_backup_${NOW}.sql.gz"
OUTPATH="${BACKUP_DIR}/${FILENAME}"

# If DATABASE_URL is present prefer it (e.g. postgres://user:pass@host:port/dbname)
if [[ -n "${DATABASE_URL:-}" ]]; then
  echo "Using DATABASE_URL"
  export PGPASSWORD="" # ensure not accidentally used
  # pg_dump understands a URL via --dbname
  pg_dump --dbname="$DATABASE_URL" --format=custom | gzip > "$OUTPATH"
else
  # Use standard PG env vars
  : "${PGHOST:?Need to set PGHOST or provide DATABASE_URL}"
  : "${PGUSER:?Need to set PGUSER or provide DATABASE_URL}"
  : "${PGDATABASE:?Need to set PGDATABASE or provide DATABASE_URL}"
  PGPORT="${PGPORT:-5432}"

  # export PGPASSWORD if provided in env; otherwise pg_dump will prompt
  if [[ -n "${PGPASSWORD:-}" ]]; then
    export PGPASSWORD="$PGPASSWORD"
  fi

  echo "Backing up ${PGDATABASE}@${PGHOST}:${PGPORT} to ${OUTPATH}"
  pg_dump -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" --format=custom | gzip > "$OUTPATH"
fi

# Check success
if [[ $? -ne 0 ]]; then
  echo "Backup failed" >&2
  exit 1
fi

# Rotate: remove backups older than RETENTION_DAYS
find "$BACKUP_DIR" -type f -name 'pg_backup_*.sql.gz' -mtime +"$RETENTION_DAYS" -exec rm -f {} \;

echo "Backup completed: $OUTPATH"
