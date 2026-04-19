# 📋 Jerico Project Documentation

## 🎯 Project Overview

**Jerico** is an advanced voice-controlled AI assistant that understands both English and Bengali. It's designed to work like Jarvis from Iron Man, executing any voice command you give it.

### Key Features
- 🎤 Voice input in English & Bengali
- 🧠 AI-powered responses using GPT-4 Turbo
- 🎯 Smart command execution (open apps, write code, etc.)
- 🔤 Multilingual support
- ⚡ Low resource usage (Python-based)
- 🔧 Easy to extend and customize

## 📁 Project Structure

```
Voice-AI-Agent/
│
├── jerico.py                 # Main agent (basic version)
├── jerico_extended.py        # Extended agent (recommended)
├── command_handler.py        # Command parsing and execution
│
├── config.json               # Configuration settings
├── requirements.txt          # Python dependencies
├── .env.example             # API key template
├── .env                     # Actual API keys (YOUR FILE)
│
├── setup.sh                 # Linux/macOS setup script
├── setup.bat                # Windows setup script
├── test_jerico.py           # Test suite
│
├── README.md                # Full documentation
├── QUICKSTART.md            # Quick start guide
├── DOCUMENTATION.md         # This file
│
└── venv/                    # Virtual environment (created during setup)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Microphone
- Internet connection
- OpenAI API key (free or premium)

### Installation (3 Steps)

1. **Clone & Setup**
   ```bash
   cd Voice-AI-Agent
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Add API Key**
   ```bash
   nano .env  # Edit and add your OpenAI API key
   ```

3. **Run Jerico**
   ```bash
   source venv/bin/activate
   python jerico_extended.py
   ```

## 📚 File Descriptions

### Core Files

#### `jerico.py` - Basic Agent
- Simple voice AI implementation
- Core listening and speaking functionality
- Basic command recognition
- Good for learning the basics

#### `jerico_extended.py` - Advanced Agent ⭐
- **RECOMMENDED** version with more features
- Advanced command parsing
- Better language detection
- Text mode for testing
- More sophisticated AI interactions
- Support for command templates

#### `command_handler.py` - Command Engine
- Parses user commands using regex patterns
- Executes system actions
- Code template generation
- Application management
- Bengali-to-English translation

### Configuration Files

#### `config.json` - Settings
```json
{
  "agent_name": "Jerico",           // Agent name
  "openai_model": "gpt-4-turbo",    // AI model
  "wake_word": "jerico",             // Voice activation word
  "timeout_seconds": 10,             // Listen timeout
  "language": "Bengali, English"      // Supported languages
}
```

#### `.env` - Secrets (YOUR FILE)
```
OPENAI_API_KEY=sk-your-key-here
```

#### `requirements.txt` - Dependencies
Lists all Python packages needed:
- speech_recognition (Google API)
- pyttsx3 (Text-to-speech)
- openai (OpenAI API client)
- python-dotenv (Environment variables)

### Setup & Testing

#### `setup.sh` / `setup.bat`
- Automated setup for different OS
- Creates virtual environment
- Installs dependencies
- Creates .env file

#### `test_jerico.py`
- Comprehensive test suite
- Verifies all installations
- Checks API configuration
- Tests microphone and audio

## 🎯 Usage Modes

### Voice Mode (Interactive Voice)
```bash
python jerico_extended.py
```
- Say "Jerico" to activate
- Give your command
- Listen for response
- Best for actual usage

### Text Mode (For Testing)
```bash
python jerico_extended.py --mode text
```
- Type commands instead of speaking
- No microphone required
- Great for debugging
- Faster for testing

## 💻 Supported Commands

### Application Management
- `"Open Chrome"` - Opens Chrome browser
- `"Open VS Code"` - Opens code editor
- `"Close Chrome"` - Closes application

### File & Code Operations
- `"Write a Python program"` - Creates Python file with template
- `"Create a file called hello.txt"` - Creates text file
- `"Create a JavaScript file"` - Creates JS template

### Web Operations
- `"Search for Python tutorial"` - Google search
- `"Open Facebook"` - Goes to website

### System Operations
- `"Take a screenshot"` - Captures screen
- `"List files"` - Shows directory contents

### Bengali Examples
- `"Chrome খুলো"` - Open Chrome
- `"পাইথন প্রোগ্রাম লিখো"` - Write Python program

## 🔧 Customization

### Change Wake Word
Edit `config.json`:
```json
"wake_word": "your_word_here"
```

### Adjust Voice Speed
Edit `config.json`:
```json
"voice_speed": 150  // Lower = slower, Higher = faster
```

### Add New Commands
Edit `command_handler.py`:
```python
COMMAND_PATTERNS = {
    'your_command': r'pattern to match',
    # ... more patterns
}
```

### Use Different AI Model
Edit `config.json`:
```json
"openai_model": "gpt-3.5-turbo"  // or any other model
```

## 🐛 Troubleshooting

### Module Not Found
```bash
pip install -r requirements.txt
```

### API Key Issues
1. Check .env file exists and is in root directory
2. Verify format: `OPENAI_API_KEY=sk-...`
3. No spaces or extra characters
4. Test at openai.com/api-keys

### Microphone Problems
```bash
python test_jerico.py
```
This will diagnose microphone issues.

### Permission Denied (Linux)
```bash
chmod +x setup.sh
chmod +x jerico*.py
```

## 📊 Technology Stack

| Component | Technology | Why? |
|-----------|-----------|------|
| Language | Python 3.8+ | Low RAM, great for voice/AI |
| Voice Input | Google Speech API | Free, accurate, multilingual |
| Voice Output | pyttsx3 | Works offline, reliable |
| AI Model | OpenAI GPT-4 | Powerful, flexible, supports ChatGPT |
| Command Parsing | Regex | Fast, customizable |
| Environment | Virtual Environment | Isolated, clean setup |

## 🌍 Language Support

### Bengali (বাংলা)
- Full voice recognition
- Text-to-speech support
- Command translation
- Bengali command patterns

### English
- Full voice recognition
- Clear text-to-speech
- Rich command set
- Default language

### Adding More Languages
1. Add language code to `config.json`
2. Add patterns to `COMMAND_PATTERNS` in `command_handler.py`
3. Update `detect_language()` in `jerico_extended.py`

## 📈 Performance

### Memory Usage
- Base: ~100 MB
- With voice listening: ~150 MB
- At peak: <500 MB (8GB recommended)

### Response Time
- Voice recognition: 2-5 seconds
- AI processing: 3-10 seconds
- Command execution: <1 second

### Cost Estimation
- Per command: ~$0.001-0.005 (depends on model)
- 100 commands/day: ~$0.30-1.50/month

## 🔐 Security Notes

1. **API Key Safety**
   - Never share .env file
   - Keep it out of git (add to .gitignore)
   - Rotate keys periodically

2. **Voice Privacy**
   - Audio is sent to Google/OpenAI
   - Check their privacy policies
   - Consider offline alternatives

3. **Command Execution**
   - Be careful with system commands
   - Restrict to trusted environment
   - Review code before execution

## 🚀 Next Steps

1. ✅ Install and setup
2. ✅ Test with text mode
3. ✅ Test with voice mode
4. ✅ Add custom commands
5. ✅ Deploy to your system

## 📞 Getting Help

1. **Check QUICKSTART.md** - Quick setup guide
2. **Read README.md** - Full documentation
3. **Run test_jerico.py** - Diagnose issues
4. **Review command_handler.py** - Understand commands
5. **Check OpenAI status** - Verify API is working

## 🎓 Learning Resources

- [OpenAI API Docs](https://platform.openai.com/docs)
- [SpeechRecognition Library](https://github.com/Uberi/speech_recognition)
- [pyttsx3 Documentation](https://pyttsx3.readthedocs.io/)
- [Python Virtual Environment](https://docs.python.org/3/tutorial/venv.html)

## 🎉 You're All Set!

Jerico is ready to be your personal AI assistant. Start by saying:

**"Jerico, open Chrome"**

Enjoy! 🤖✨

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Maintained by:** Jerico Team
