#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip to latest version
pip install --upgrade pip

# Install requirements with more flexible version handling
pip install -r requirements.txt --no-cache-dir

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
