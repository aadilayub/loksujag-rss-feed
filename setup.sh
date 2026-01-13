#!/bin/bash
# Quick setup script for Loksujag RSS Scraper

set -e

echo "🚀 Setting up Loksujag RSS Scraper..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the scraper:"
echo "  source venv/bin/activate"
echo "  python scraper.py"
echo ""
echo "To deploy to GitHub:"
echo "  1. Create a new GitHub repository"
echo "  2. git init"
echo "  3. git add ."
echo "  4. git commit -m 'Initial commit'"
echo "  5. git remote add origin <your-repo-url>"
echo "  6. git push -u origin main"
echo "  7. Enable GitHub Actions and GitHub Pages in repo settings"
echo ""
