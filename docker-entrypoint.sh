#!/bin/bash
set -e

echo "Starting Weather Dashboard container..."

# Initialize the database
echo "Initializing database..."
python /app/init_db.py

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8008 --workers=4 --access-logfile - --error-logfile - --log-level=debug --timeout 120 run:app
