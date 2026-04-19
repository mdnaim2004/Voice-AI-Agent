#!/bin/bash
# Jerico Installation Guide for Linux
# Complete step-by-step installation

set -e

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║  🤖 JERICO VOICE AI AGENT - LINUX SETUP      ║"
echo "║  Complete Installation Guide                  ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Step 1: Check system prerequisites
echo "Step 1: Checking system prerequisites..."
echo "========================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo "Install with: sudo apt-get install python3 python3-dev python3-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION found"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found!"
    echo "Install with: sudo apt-get install python3-pip"
    exit 1
fi

echo "✅ pip3 is installed"

# Step 2: Install system dependencies
echo ""
echo "Step 2: Installing system dependencies..."
echo "=========================================="

# Audio libraries for voice
echo "Installing audio libraries..."
sudo apt-get update -qq
sudo apt-get install -y python3-dev libportaudio2 portaudio19-dev
echo "✅ Audio libraries installed"

# Step 3: Navigate to project
echo ""
echo "Step 3: Setting up Jerico directory..."
echo "========================================"

PROJECT_DIR="/home/mdnaim2004/mydesk/Voice-AI-Agent/Voice-AI-Agent"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Project directory not found!"
    exit 1
fi

cd "$PROJECT_DIR"
echo "✅ In project directory: $PROJECT_DIR"

# Step 4: Create virtual environment
echo ""
echo "Step 4: Creating virtual environment..."
echo "========================================"

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "⚠️  Virtual environment already exists"
fi

# Step 5: Activate virtual environment
echo ""
echo "Step 5: Activating virtual environment..."
echo "=========================================="

source venv/bin/activate
echo "✅ Virtual environment activated"
echo "   Run this in future: source venv/bin/activate"

# Step 6: Upgrade pip
echo ""
echo "Step 6: Upgrading pip..."
echo "========================"

pip install --upgrade pip setuptools wheel -q
echo "✅ pip upgraded"

# Step 7: Install Python dependencies
echo ""
echo "Step 7: Installing Python dependencies..."
echo "=========================================="

echo "This may take a few minutes..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ All dependencies installed successfully"
else
    echo "⚠️  Some dependencies had issues (may still work)"
fi

# Step 8: Setup .env file
echo ""
echo "Step 8: Setting up configuration..."
echo "===================================="

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ .env file created from template"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your OpenAI API key!"
    echo "   Command: nano .env"
    echo "   Then add your key to: OPENAI_API_KEY=sk-..."
else
    echo "✅ .env file already exists"
fi

# Step 9: Run tests
echo ""
echo "Step 9: Running tests..."
echo "======================="

python test_jerico.py

# Step 10: Final instructions
echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║  ✅ SETUP COMPLETE!                           ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "📋 Next Steps:"
echo "1. Edit .env file with your OpenAI API key:"
echo "   nano .env"
echo ""
echo "2. Run Jerico:"
echo "   python jerico_extended.py"
echo ""
echo "3. To activate environment next time:"
echo "   source venv/bin/activate"
echo ""
echo "💡 For text-based testing (no microphone needed):"
echo "   python jerico_extended.py --mode text"
echo ""
echo "📚 Documentation:"
echo "   - QUICKSTART.md - Quick start guide"
echo "   - README.md - Full documentation"
echo "   - DOCUMENTATION.md - Technical details"
echo ""
echo "🎯 Ready to start? Say 'Jerico' and command!"
echo ""
