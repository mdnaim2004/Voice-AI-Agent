# 🤖 Jerico - Voice AI Agent

A powerful voice-controlled AI assistant that understands both **Bengali** and **English** commands. Named after the biblical city of Jericho, Jerico acts like Jarvis from Iron Man, executing any task you command it to do!

## Features

✨ **Voice Commands** - Speak in Bengali or English  
🎯 **Smart Command Execution** - Open apps, write code, create files  
🧠 **AI-Powered** - Powered by OpenAI's GPT-4 Turbo  
🎤 **Voice I/O** - Listen and respond with realistic speech  
⚡ **Low Resource Usage** - Optimized for Python (lighter than Node.js)  
🔧 **Keyboard Shortcuts** - Press 'J' to activate anytime  
🌍 **Multilingual** - Bengali and English support  

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Memory**: Minimum 4 GB RAM (8 GB recommended)
- **Disk Space**: Minimum 1 GB free
- **Python**: 3.8 or later
- **Microphone**: Required for voice input

## Installation

### Step 1: Clone the Repository

```bash
cd /home/mdnaim2004/mydesk/Voice-AI-Agent
git clone https://github.com/mdnaim2004/Voice-AI-Agent.git
cd Voice-AI-Agent
```

### Step 2: Set Up Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note for Linux users:** You may need to install additional system dependencies:
```bash
sudo apt-get install python3-dev libportaudio2 portaudio19-dev
```

### Step 4: Configure OpenAI API Key

1. Get your OpenAI API key from [OpenAI Dashboard](https://platform.openai.com/api-keys)
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your API key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

## Quick Start

### Run Jerico

```bash
python jerico.py
```

### Usage Examples

**Activate Jerico:**
- Say "Jerico" to wake it up
- OR press the **'J'** key to activate

**Example Commands:**

In **English:**
- "Open Chrome"
- "Open VS Code"
- "Write a Python function"
- "Take a screenshot"
- "Open Facebook"

In **Bengali (বাংলা):**
- "Chrome খুলো" (Open Chrome)
- "একটি পাইথন প্রোগ্রাম লিখো" (Write a Python program)
- "VS Code খুলো" (Open VS Code)
- "Facebook খুলো" (Open Facebook)

## Configuration

Edit `config.json` to customize:

```json
{
  "agent_name": "Jerico",
  "language": "Bengali, English",
  "openai_model": "gpt-4-turbo",
  "wake_word": "jerico",
  "timeout_seconds": 10,
  "supported_actions": [
    "open_application",
    "write_file",
    "execute_command",
    "web_search",
    "screenshot"
  ]
}
```

## Supported Actions

| Action | Description |
|--------|-------------|
| `open_application` | Open apps like Chrome, VS Code, Firefox |
| `write_file` | Create and write Python, JavaScript, etc. |
| `execute_command` | Run system commands |
| `web_search` | Search the internet |
| `screenshot` | Capture screen |
| `open_browser` | Open websites |
| `close_application` | Close running apps |

## Troubleshooting

### Issue: "Module not found" errors
**Solution:** Reinstall requirements and ensure virtual environment is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Microphone not detected
**Solution:** Check microphone permissions and test with:
```bash
python -m speech_recognition
```

### Issue: OpenAI API errors
**Solution:** Verify your API key is correct in `.env` file

### Issue: Slow response
**Solution:** Ensure you have a good internet connection for API calls

## Project Structure

```
Voice-AI-Agent/
├── jerico.py              # Main agent application
├── config.json            # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # API key template
├── README.md             # This file
└── venv/                 # Virtual environment
```

## Technology Stack

- **Language**: Python 3.8+
- **Speech Recognition**: Google Speech-to-Text API
- **Text-to-Speech**: pyttsx3
- **AI Model**: OpenAI GPT-4 Turbo
- **Voice Input**: SpeechRecognition library
- **System Control**: pynput, subprocess

## Why Python?

✅ **Lower RAM Usage** - Python is more efficient than Node.js  
✅ **Better for AI/ML** - Extensive ML libraries  
✅ **Simpler Deployment** - Easy to run on any platform  
✅ **Perfect for Voice Processing** - Mature speech libraries  

## API Usage Notes

- Jerico uses OpenAI's API, so check your usage limits
- Each command uses roughly 100-500 tokens
- Keep your API key secure!

## Features Coming Soon

🔜 Advanced file creation with code generation  
🔜 Web scraping and information retrieval  
🔜 Screenshot analysis with vision  
🔜 System automation scripts  
🔜 Custom skill training  
🔜 Offline mode with local TTS  

## Contributing

Found a bug or want to add a feature? Open an issue or submit a pull request!

## License

MIT License - Feel free to use Jerico for personal or commercial projects

## Support

If you encounter issues:
1. Check the Troubleshooting section
2. Review your `.env` configuration
3. Ensure all dependencies are installed
4. Test your microphone and internet connection

---

**Made with ❤️ by Jerico Team**  
*Your Voice, Your Commands, Your Assistant!*