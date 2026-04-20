import os
import json
import sys
import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import google.generativeai as genai
import subprocess
import webbrowser
from pathlib import Path
from dotenv import load_dotenv
import threading
from pynput import keyboard
from contextlib import contextmanager
import ctypes
import argparse

# Load environment variables
load_dotenv()


def _alsa_error_handler(filename, line, function, err, fmt):
    # Intentionally no-op to silence verbose native ALSA warnings.
    return


@contextmanager
def suppress_alsa_warnings():
    """Temporarily suppress low-level ALSA error spam on Linux."""
    asound = None
    c_handler = None
    stderr_fd = None
    devnull_fd = None
    try:
        asound = ctypes.cdll.LoadLibrary("libasound.so")
        handler_type = ctypes.CFUNCTYPE(
            None,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
        )
        c_handler = handler_type(_alsa_error_handler)
        asound.snd_lib_error_set_handler(c_handler)
    except Exception:
        # If ALSA hooks are unavailable, continue without suppression.
        pass

    try:
        # Mute native JACK/ALSA C-library stderr noise for this critical section.
        try:
            stderr_fd = os.dup(2)
            devnull_fd = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull_fd, 2)
        except Exception:
            stderr_fd = None
            devnull_fd = None
        yield
    finally:
        if stderr_fd is not None:
            try:
                os.dup2(stderr_fd, 2)
            except Exception:
                pass
        if devnull_fd is not None:
            try:
                os.close(devnull_fd)
            except Exception:
                pass
        if stderr_fd is not None:
            try:
                os.close(stderr_fd)
            except Exception:
                pass
        if asound is not None:
            try:
                asound.snd_lib_error_set_handler(None)
            except Exception:
                pass

class JericoAgent:
    def __init__(self):
        """Initialize Jerico Voice AI Agent"""
        self.config = self.load_config()
        self.api_provider = self.config.get('api_provider', 'gemini').lower()
        self.recognizer = sr.Recognizer()
        with suppress_alsa_warnings():
            self.microphone = sr.Microphone()
        
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speech rate
        
        # Initialize AI backend
        self.openai_client = None
        self.model_candidates = self._build_model_candidates()
        self.ai_available = False
        self._init_ai_backend()
        
        self.is_listening = False
        self.current_language = "en"  # Default language
        
        print("🤖 Jerico Voice AI Agent initialized!")
        print(f"Version: {self.config['version']}")
        print(f"Agent Name: {self.config['agent_name']}")
        print(f"AI Provider: {self.api_provider}")
        print("Say 'Jerico' to wake me up, or press 'J' key to activate...")

    def _build_model_candidates(self):
        """Build ordered model fallback list for current AI provider."""
        if self.api_provider == 'gemini':
            configured = self.config.get('gemini_model', 'gemini-1.5-flash')
            fallbacks = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-2.0-flash']
        else:
            configured = self.config.get('openai_model', 'gpt-4o-mini')
            fallbacks = ['gpt-4o-mini', 'gpt-4.1-mini', 'gpt-4o']
        ordered = [configured] + [m for m in fallbacks if m != configured]
        return ordered

    def _init_ai_backend(self):
        """Initialize selected AI backend client."""
        if self.api_provider == 'gemini':
            api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
            if not api_key:
                print("⚠️ GEMINI_API_KEY not found. Running in local fallback mode.")
                return
            genai.configure(api_key=api_key)
            self.ai_available = True
            return

        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("⚠️ OPENAI_API_KEY not found. Running in local fallback mode.")
            return

        self.openai_client = OpenAI(api_key=api_key)
        self.ai_available = True

    def _is_model_not_available_error(self, error):
        """Return True when provider rejects model name or access."""
        msg = str(error).lower()
        markers = [
            'model_not_found',
            'does not exist',
            'you do not have access',
            'unsupported_model',
            'not found for api version',
            'permission denied for model',
        ]
        return any(marker in msg for marker in markers)

    def _categorize_ai_error(self, error):
        """Classify common AI provider failures for user-friendly fallback handling."""
        msg = str(error).lower()
        if 'insufficient_quota' in msg or 'exceeded your current quota' in msg:
            return 'quota'
        if 'rate_limit' in msg or 'too many requests' in msg:
            return 'rate_limit'
        if 'invalid_api_key' in msg or 'incorrect api key' in msg:
            return 'auth'
        if self._is_model_not_available_error(error):
            return 'model'
        return 'other'

    def _offline_fallback_response(self, user_input, reason='other'):
        """Provide a basic local fallback when cloud AI is unavailable."""
        responses = {
            'quota': (
                "AI quota is exhausted right now. I can still run local commands "
                "like opening apps and websites."
            ),
            'rate_limit': (
                "AI rate limit is currently reached. Please try again in a moment. "
                "Local commands still work."
            ),
            'auth': (
                "API key appears invalid or missing. Please check your .env file."
            ),
            'model': (
                "The configured AI model is not available for this account. "
                "I can continue with local commands."
            ),
            'other': (
                "The AI service is temporarily unavailable. I can still help with local commands."
            ),
        }

        normalized = user_input.strip().lower()
        small_talk = {
            'hello': "Hello! I am running in local fallback mode right now.",
            'hi': "Hi! AI is unavailable at the moment, but I can still run local actions.",
            'how are you': "I am operational. AI cloud access is currently limited.",
        }

        if normalized in small_talk:
            return f"{small_talk[normalized]} {responses.get(reason, responses['other'])}"

        return responses.get(reason, responses['other'])

    def _create_openai_completion_with_fallback(self, system_prompt, user_input):
        """Try configured OpenAI model first, then compatible alternatives."""
        last_error = None

        for model_name in self.model_candidates:
            try:
                response = self.openai_client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )

                if model_name != self.config.get('openai_model', 'gpt-4o-mini'):
                    print(f"ℹ️ Falling back to available model: {model_name}")

                return response
            except Exception as err:
                last_error = err
                if not self._is_model_not_available_error(err):
                    raise

        raise last_error

    def _extract_gemini_text(self, response):
        """Safely extract text from Gemini response object."""
        text = getattr(response, 'text', None)
        if text:
            return text.strip()

        candidates = getattr(response, 'candidates', None) or []
        for candidate in candidates:
            content = getattr(candidate, 'content', None)
            parts = getattr(content, 'parts', None) or []
            assembled = []
            for part in parts:
                part_text = getattr(part, 'text', None)
                if part_text:
                    assembled.append(part_text)
            if assembled:
                return "\n".join(assembled).strip()

        return None

    def _create_gemini_completion_with_fallback(self, system_prompt, user_input):
        """Try configured Gemini model first, then compatible alternatives."""
        last_error = None

        for model_name in self.model_candidates:
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_prompt,
                )
                response = model.generate_content(user_input)
                response_text = self._extract_gemini_text(response)
                if response_text:
                    if model_name != self.config.get('gemini_model', 'gemini-1.5-flash'):
                        print(f"ℹ️ Falling back to available model: {model_name}")
                    return response_text
                raise RuntimeError("Empty response returned by Gemini model")
            except Exception as err:
                last_error = err
                if not self._is_model_not_available_error(err):
                    raise

        raise last_error

    def _generate_ai_response(self, system_prompt, user_input):
        """Generate AI response from selected provider with model fallback."""
        if self.api_provider == 'gemini':
            return self._create_gemini_completion_with_fallback(system_prompt, user_input)

        response = self._create_openai_completion_with_fallback(system_prompt, user_input)
        return response.choices[0].message.content
    
    def load_config(self):
        """Load configuration from config.json"""
        config_path = Path(__file__).parent / "config.json"
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"🎤 Jerico: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self, language="en-US"):
        """Listen to user voice input"""
        try:
            print(f"👂 Listening... ({language})")
            with suppress_alsa_warnings(), self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen with timeout
                audio = self.recognizer.listen(
                    source, 
                    timeout=self.config['timeout_seconds'],
                    phrase_time_limit=10
                )
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio, language=language)
            print(f"📝 You said: {text}")
            return text.lower()
        
        except sr.UnknownValueError:
            response = "Sorry, I didn't understand that. Please try again."
            self.speak(response)
            return None
        except sr.RequestError:
            response = "Sorry, I couldn't reach the speech recognition service."
            self.speak(response)
            return None
        except sr.WaitTimeoutError:
            return None
    
    def detect_language(self, text):
        """Detect if text is Bengali or English"""
        # Simple detection: Bengali characters are in a specific Unicode range
        bengali_unicode_start = 0x0980
        bengali_unicode_end = 0x09FF
        
        bengali_count = sum(1 for char in text if bengali_unicode_start <= ord(char) <= bengali_unicode_end)
        
        if bengali_count > len(text) * 0.3:  # If more than 30% is Bengali
            return "bn"
        return "en"
    
    def process_command(self, user_input):
        """Process user command using selected AI provider."""
        try:
            # Detect language
            language = self.detect_language(user_input)
            self.current_language = language

            if not self.ai_available:
                return self._offline_fallback_response(user_input, reason='auth')
            
            system_prompt = self._get_system_prompt(language)
            return self._generate_ai_response(system_prompt, user_input)
        
        except Exception as e:
            category = self._categorize_ai_error(e)
            error_msg = f"Error processing command: {str(e)}"
            print(f"❌ {error_msg}")
            return self._offline_fallback_response(user_input, reason=category)
    
    def _get_system_prompt(self, language="en"):
        """Get system prompt based on language"""
        if language == "bn":
            return """আপনি একজন ভয়েস এআই সহায়ক যার নাম Jerico। আপনার কাজ হল ব্যবহারকারীর কথা শুনে এবং তাদের অনুরোধ অনুযায়ী কাজ করা। 
            আপনি বাংলায় সাড়া দিন। আপনি অ্যাপ্লিকেশন খুলতে, ফাইল তৈরি করতে, ওয়েব সার্চ করতে এবং অন্যান্য অনেক কাজ করতে পারেন।
            সবসময় সংক্ষিপ্ত এবং সহায়ক উত্তর দিন।"""
        else:
            return """You are a voice AI assistant named Jerico. Your job is to listen to user commands and perform tasks accordingly.
            You can open applications, create files, perform web searches, take screenshots, and much more.
            Always provide clear, concise, and helpful responses. Respond in English."""
    
    def execute_action(self, command):
        """Execute system actions based on commands"""
        command_lower = command.lower()
        
        # Open applications
        if "open" in command_lower:
            if "chrome" in command_lower or "google" in command_lower:
                self._open_application("google-chrome")
                return "Opening Chrome browser"
            elif "firefox" in command_lower:
                self._open_application("firefox")
                return "Opening Firefox"
            elif "vs code" in command_lower or "vscode" in command_lower:
                self._open_application("code")
                return "Opening VS Code"
            elif "facebook" in command_lower:
                webbrowser.open("https://facebook.com")
                return "Opening Facebook"
            elif "youtube" in command_lower:
                webbrowser.open("https://youtube.com")
                return "Opening YouTube"
            elif "word" in command_lower:
                self._open_application("libreoffice --writer")
                return "Opening LibreOffice Writer"
        
        # Write/create files
        elif "write" in command_lower or "create" in command_lower:
            return "I can help you write code or create files. Please specify what you'd like to create."
        
        # Take screenshot
        elif "screenshot" in command_lower or "screen" in command_lower:
            return "Screenshot functionality to be implemented"
        
        # Close application
        elif "close" in command_lower or "exit" in command_lower:
            return "I'll close the requested application"
        
        return None
    
    def _open_application(self, app_name):
        """Open an application"""
        try:
            subprocess.Popen(app_name.split())
        except Exception as e:
            print(f"Error opening {app_name}: {e}")
    
    def wake_word_detection(self, text):
        """Check if wake word is present"""
        return self.config['wake_word'].lower() in text.lower()
    
    def run(self):
        """Run Jerico in voice mode"""
        print("\n🎯 Jerico is ready! Say 'Jerico' to activate, or press 'J' key...")
        print("Say 'quit' or 'exit' to stop, or press Ctrl+C.\n")
        
        listener = keyboard.Listener(on_press=self.on_key_press)
        listener.start()
        
        try:
            while True:
                # Listen for command
                user_input = self.listen("en-US")
                
                if not user_input:
                    continue

                if user_input.strip().lower() in {"quit", "exit", "bye"}:
                    self.speak("Goodbye!")
                    break
                
                # Check for wake word
                if not self.wake_word_detection(user_input):
                    continue
                
                print(f"✅ Jerico activated!")
                self.speak("I'm listening. What would you like me to do?")
                
                # Listen for actual command
                command = self.listen("en-US")
                
                if not command:
                    continue

                if command.strip().lower() in {"quit", "exit", "bye"}:
                    self.speak("Goodbye!")
                    break
                
                # Try to execute action first
                action_response = self.execute_action(command)
                
                if action_response:
                    self.speak(action_response)
                else:
                    # Process with AI
                    response = self.process_command(command)
                    self.speak(response)
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        finally:
            listener.stop()

    def run_text_mode(self):
        """Run Jerico in text mode (no microphone required)."""
        print("\n📝 Text mode active. Type commands and press Enter.")
        print("Type 'quit' or 'exit' to stop.\n")

        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Goodbye!")
                break

            if not user_input:
                continue

            if user_input.lower() in {"quit", "exit", "bye"}:
                self.speak("Goodbye!")
                break

            action_response = self.execute_action(user_input)
            if action_response:
                self.speak(action_response)
                continue

            response = self.process_command(user_input)
            self.speak(response)
    
    def on_key_press(self, key):
        """Handle keyboard shortcuts"""
        try:
            if key.char == 'j' or key.char == 'J':
                print("\n🎤 Activation key pressed! Listening now...")
                command = self.listen("en-US")
                if command:
                    response = self.process_command(command)
                    self.speak(response)
        except AttributeError:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jerico Voice AI Agent")
    parser.add_argument(
        "--mode",
        choices=["voice", "text"],
        default="voice",
        help="Run in voice mode or text mode (default: voice)",
    )
    args = parser.parse_args()

    agent = JericoAgent()
    if args.mode == "text":
        agent.run_text_mode()
    else:
        agent.run()
