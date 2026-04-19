@echo off
REM Jerico Voice AI Agent Setup Script for Windows
REM This script sets up Jerico for you automatically

echo.
echo 🤖 Welcome to Jerico Voice AI Agent Setup!
echo ===========================================
echo.

REM Check Python version
echo 📌 Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ from python.org
    exit /b 1
)

REM Create virtual environment
echo.
echo 📌 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo.
echo 📌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo 📌 Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo 📌 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env and add your OpenAI API key!
)

echo.
echo ✅ Setup complete!
echo.
echo 📝 Next steps:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Run: venv\Scripts\activate.bat
echo 3. Run: python jerico.py
echo.
echo 💡 To deactivate virtual environment later, type: deactivate
