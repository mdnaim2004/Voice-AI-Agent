#!/bin/bash

# Jerico Voice AI Agent Setup Script
# This script sets up Jerico for you automatically

echo "🤖 Welcome to Jerico Voice AI Agent Setup!"
echo "==========================================="
echo ""

# Check Python version
echo "📌 Checking Python version..."
python3 --version || { echo "❌ Python 3 not found. Please install Python 3.8+"; exit 1; }

# Create virtual environment
echo ""
echo "📌 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo ""
echo "📌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📌 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📌 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OpenAI API key!"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python jerico.py"
echo ""
echo "💡 To deactivate virtual environment later, type: deactivate"
