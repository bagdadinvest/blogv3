#!/bin/bash

# Set variables for SQLite and PostgreSQL
SQLITE_DB_PATH="db.sqlite3"  # Path to your SQLite database
POSTGRES_URL="postgresql://lotfikan:your_secure_password@localhost:5432/dentidelil"  # Update with your PostgreSQL details
PGLOADER_CONFIG="pgloader_migration.load"  # Temporary pgloader configuration file

# Check if SQLite database exists
if [ ! -f "$SQLITE_DB_PATH" ]; then
    echo "Error: SQLite database not found at $SQLITE_DB_PATH"
    exit 1
fi

# Generate the pgloader configuration file
cat > $PGLOADER_CONFIG << EOF
LOAD DATABASE
     FROM sqlite:///$SQLITE_DB_PATH
     INTO $POSTGRES_URL

WITH
     include no drop,
     create tables,
     create indexes,
     reset sequences

SET work_mem to '32MB',
    maintenance_work_mem to '512MB'

CAST
     type uuid to uuid
     drop default drop not null,
     type text to text,
     type integer to integer,
     type real to real,
     type blob to bytea;

ALTER SCHEMA main RENAME TO public;
EOF

# Execute pgloader
echo "Starting migration from SQLite to PostgreSQL..."
pgloader $PGLOADER_CONFIG

# Clean up temporary configuration file
rm -f $PGLOADER_CONFIG

echo "Migration completed successfully. Please verify the PostgreSQL database."
exit 0
