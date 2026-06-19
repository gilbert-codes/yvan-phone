#!/usr/bin/env bash
set -o errexit

echo "🐍 Python version:"
python --version

echo "📦 Installing Cloudinary explicitly..."
pip install cloudinary==1.44.2 django-cloudinary-storage==0.3.0 pillow==12.2.0

echo "📦 Installing all dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

echo "🔄 Running migrations..."
python manage.py migrate

echo "✅ Build complete!"