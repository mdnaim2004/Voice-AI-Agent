# Jerico - Voice AI Agent

Jerico is a bilingual (Bangla + English) voice assistant with local action handling and cloud AI responses.

Current defaults:
- AI provider: Gemini
- TTS provider: Edge TTS (with automatic fallback to pyttsx3)
- Local mode fallback: enabled when cloud quota/API is unavailable

## Features

- Voice and text mode
- Bangla + English command support
- Gemini or OpenAI backend support
- Edge neural TTS with pyttsx3 fallback
- App/web action shortcuts (Chrome, YouTube, Facebook, VS Code)

## Requirements

- **OS**: Windows, macOS, or Linux
- **Memory**: Minimum 4 GB RAM (8 GB recommended)
- **Disk Space**: Minimum 1 GB free
- Python 3.8+
- Microphone (only for voice mode)
- Internet connection for Gemini/OpenAI and Edge TTS

## Setup

### 1. Create venv and install packages

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

For Linux, install audio/system dependencies if needed:
```bash
sudo apt-get update
sudo apt-get install -y python3-dev libportaudio2 portaudio19-dev ffmpeg
```

`ffmpeg` provides `ffplay` which Jerico uses for Edge TTS playback.

### 2. Configure API key

Gemini (default):
```bash
  cp .env.example .env
```

Add in `.env`:
```env
GEMINI_API_KEY=your-gemini-api-key
```

Optional OpenAI setup:

```env
OPENAI_API_KEY=your-openai-key
```

If you want OpenAI as primary provider, set in `config.json`:

```json
"api_provider": "openai"
```

## Run

Recommended first run (text mode):

```bash
python jerico.py --mode text
```

Voice mode:

```bash
python jerico.py --mode voice
```

## Usage Examples

Wake voice mode by saying `jerico` or pressing `J`.

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

## Key Configuration

`config.json` example:

```json
{
  "agent_name": "Jerico",
  "api_provider": "gemini",
  "gemini_model": "gemini-1.5-flash",
  "openai_model": "gpt-4o-mini",
  "tts_provider": "edge",
  "edge_tts_voice_en": "en-US-EmmaMultilingualNeural",
  "edge_tts_voice_bn": "bn-BD-NabanitaNeural",
  "wake_word": "jerico",
  "timeout_seconds": 10
}
```

## Troubleshooting (Important)

### Problem: "API key missing" or fallback response only
Fix:
1. Ensure `.env` exists.
2. If `api_provider` is `gemini`, add `GEMINI_API_KEY=...`.
3. If you only have `OPENAI_API_KEY`, Jerico will fall back to OpenAI automatically.
4. Restart app.
5. If both cloud providers fail, Jerico still works in local mode for time/date/help/app actions.

### Problem: Voice sounds same/robotic
Cause: Edge TTS is not active; app fell back to pyttsx3.
Fix:
1. Install player: `sudo apt install -y ffmpeg`
2. Ensure internet is available for Edge TTS.
3. Keep `"tts_provider": "edge"` in `config.json`.

### Problem: Voice mode not working
Fix:
1. Test in text mode first: `python jerico.py --mode text`
2. Check microphone permissions.
3. Jerico now auto-falls back to text mode if mic is unavailable.

### Problem: Gemini errors/quota
Fix:
1. Verify key in `.env`.
2. Check model name in `config.json`.
3. Check Google AI Studio quota/limits.
4. If `OPENAI_API_KEY` is also set, Jerico will automatically fall back to OpenAI when Gemini is rate-limited.

### Problem: OpenAI errors
Fix:
1. Set `"api_provider": "openai"`.
2. Add `OPENAI_API_KEY`.
3. Check OpenAI billing/quota.

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

## Tech Stack

- Python 3
- SpeechRecognition + PyAudio
- Gemini/OpenAI APIs
- Edge TTS + pyttsx3 fallback
- pynput + subprocess for actions

## License

MIT License - Feel free to use Jerico for personal or commercial projects

## Support

If you face issues:
1. Run text mode first.
2. Validate `.env` keys.
3. Check troubleshooting section above.
4. Share terminal output for faster debugging.

---

Made by Jerico Team