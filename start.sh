#!/usr/bin/env bash
# exit on error
set -o errexit

# Get the port from environment variable or default to 8000
PORT=${PORT:-8000}

echo "Starting Django server on port $PORT..."
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Django version: $(python -c 'import django; print(django.get_version())')"

# Run the Django development server
exec python manage.py runserver 0.0.0.0:$PORT --noreload 