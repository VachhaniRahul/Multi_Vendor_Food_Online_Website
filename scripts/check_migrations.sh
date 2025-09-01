#!/bin/bash
set -e

# Run Django makemigrations check
echo "Checking for missing migrations..."
python manage.py makemigrations --check --dry-run
