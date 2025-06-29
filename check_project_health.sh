#!/bin/bash

echo "🩺 Running CodeVerse Project Health Check..."

echo "🔍 Checking Python syntax..."
find . -name "*.py" ! -path "./codeverse-env/*" | xargs python -m py_compile || exit 1

echo "🧠 Django check..."
python manage.py check || exit 1

echo "🧱 Making sure migrations are fine..."
python manage.py makemigrations --dry-run --check || exit 1

echo "🧪 Running tests..."
python manage.py test || exit 1

echo "✅ All checks passed! You're good to go."