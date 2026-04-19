# 🚀 Jerico Quick Start Guide

## 1️⃣ Get Your OpenAI API Key

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign in with your account (or create one)
3. Click "Create new secret key"
4. Copy the key (you'll only see it once!)

## 2️⃣ Setup Jerico (Choose Your OS)

### 🐧 Linux / macOS

```bash
# Navigate to the project
cd /home/mdnaim2004/mydesk/Voice-AI-Agent/Voice-AI-Agent

# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### 🪟 Windows

```bash
# Navigate to the project
cd Voice-AI-Agent

# Run setup
setup.bat
```

## 3️⃣ Configure API Key

```bash
# Edit .env file
nano .env              # Linux/macOS
notepad .env           # Windows
```

Replace `your_openai_api_key_here` with your actual API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

Save and exit.

## 4️⃣ Activate Virtual Environment

### 🐧 Linux / macOS
```bash
source venv/bin/activate
```

### 🪟 Windows
```bash
venv\Scripts\activate
```

## 5️⃣ Run Jerico

### Voice Mode (Recommended)
```bash
python jerico_extended.py
```

### Interactive Text Mode (For Testing)
```bash
python jerico_extended.py --mode text
```

## 6️⃣ Start Using Jerico

### Voice Commands
1. **Activate**: Say "Jerico" to wake up
2. **Give Command**: Say what you want to do
3. **Listen**: Jerico will respond

### Example Commands

**English:**
```
"Open Chrome"
"Write a Python program"
"Search for Python tutorial"
"Create a file called hello.txt"
"Close Chrome"
```

**Bengali (বাংলা):**
```
"Chrome খুলো" (Open Chrome)
"একটি পাইথন প্রোগ্রাম লিখো" (Write Python program)
"Google এ অনুসন্ধান করো" (Search on Google)
```

## ⚙️ Troubleshooting

### Microphone Not Working?
```bash
# Test microphone
python -c "import speech_recognition; print('Microphone OK')"
```

### API Key Issues?
- Check `.env` file has correct format
- Ensure no extra spaces or quotes
- Verify API key is active at openai.com

### Module Errors?
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Audio Not Playing?
```bash
# Check audio settings
python -c "import pyttsx3; engine = pyttsx3.init(); engine.say('Test'); engine.runAndWait()"
```

## 📚 Advanced Usage

### Interactive Mode for Testing
```bash
python jerico_extended.py --mode text
```
This lets you test commands without voice.

### View Logs
```bash
# Enable debug mode in config.json
# Set "debug_mode": true
```

## 🎯 Pro Tips

1. **Speak clearly** - Proper pronunciation helps voice recognition
2. **Use simple commands** - More specific = better execution
3. **Test first** - Use text mode before voice mode
4. **Keep .env secure** - Never share your API key!
5. **Monitor API usage** - Check OpenAI dashboard for cost

## 🔧 Customize Jerico

Edit `config.json` to:
- Change wake word (default: "jerico")
- Adjust voice speed
- Add more AI models
- Configure timeout

## 📞 Need Help?

1. Check README.md for full documentation
2. Review Troubleshooting section
3. Check OpenAI API status
4. Verify internet connection

## 🎉 You're Ready!

Jerico is now installed and ready to use. Say "Jerico" and start commanding!

**Enjoy your personal AI assistant!** 🤖✨
