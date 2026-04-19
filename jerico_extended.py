"""
Jerico Voice AI Agent - Extended Version
Enhanced with advanced command handling and language support
"""

import os
import json
import sys
import speech_recognition as sr
import pyttsx3
from openai import OpenAI
from command_handler import CommandHandler, translate_bengali_command
from pathlib import Path
from dotenv import load_dotenv
import threading

# Load environment variables
load_dotenv()

class JericoExtended:
    def __init__(self):
        """Initialize Jerico Extended Voice AI Agent"""
        self.config = self.load_config()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.9)
        
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY not found in .env file!")
        
        self.openai_client = OpenAI(api_key=api_key)
        self.current_language = "en"
        self.is_active = False
        
        self._print_welcome()
    
    def load_config(self):
        """Load configuration from config.json"""
        config_path = Path(__file__).parent / "config.json"
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def _print_welcome(self):
        """Print welcome message"""
        banner = """
╔═══════════════════════════════════════════╗
║   🤖 JERICO - VOICE AI AGENT 🤖          ║
║   Your Personal AI Assistant              ║
║                                           ║
║   Version: 1.0.0                          ║
║   Status: Ready for voice commands        ║
╚═══════════════════════════════════════════╝

Commands:
  🎤 Say 'Jerico' to wake me up
  🔤 Speak in English or Bengali
  🎯 Ask me to open apps, write code, etc.
  
Examples:
  - "Open Chrome"
  - "Write a Python program"
  - "Chrome খুলো" (Bengali)
  
Type 'quit' or 'exit' to stop.
        """
        print(banner)
    
    def speak(self, text, force_language=None):
        """Convert text to speech"""
        try:
            # Detect language if not specified
            if not force_language:
                force_language = self.detect_language(text)
            
            print(f"\n🎤 Jerico: {text}\n")
            
            if force_language == "bn":
                # For Bengali, we'd need specialized TTS
                print("   [Bengali TTS would be used here]")
            
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"⚠️  Error in text-to-speech: {e}")
    
    def listen(self, language="en-US"):
        """Listen to user voice input"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print(f"👂 Listening ({language})...")
                
                audio = self.recognizer.listen(
                    source,
                    timeout=self.config['timeout_seconds'],
                    phrase_time_limit=10
                )
            
            text = self.recognizer.recognize_google(audio, language=language)
            print(f"📝 You said: {text}")
            return text.lower()
        
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't understand. Please try again.")
            return None
        except sr.RequestError as e:
            self.speak("I couldn't reach the speech service. Check your internet.")
            return None
        except sr.Timeout:
            return None
    
    def detect_language(self, text):
        """Detect language (Bengali or English)"""
        bengali_unicode_start = 0x0980
        bengali_unicode_end = 0x09FF
        
        bengali_count = sum(1 for char in text if bengali_unicode_start <= ord(char) <= bengali_unicode_end)
        
        return "bn" if bengali_count > len(text) * 0.3 else "en"
    
    def process_with_ai(self, user_input):
        """Process command with OpenAI"""
        language = self.detect_language(user_input)
        
        try:
            system_prompt = self._get_system_prompt(language)
            
            response = self.openai_client.chat.completions.create(
                model=self.config['openai_model'],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            error_msg = f"Error with OpenAI API: {str(e)}"
            print(f"❌ {error_msg}")
            return "I encountered an error processing your request."
    
    def _get_system_prompt(self, language="en"):
        """Get context-aware system prompt"""
        if language == "bn":
            return """আপনি Jerico, একটি উন্নত ভয়েস AI সহায়ক। আপনার কাজ হল ব্যবহারকারীর বাংলা কমান্ড বুঝা এবং সেগুলি সম্পাদন করা।
            আপনি অ্যাপ্লিকেশন খুলতে, কোড লিখতে, ফাইল তৈরি করতে এবং আরও অনেক কিছু করতে পারেন।
            সর্বদা বাংলায় সংক্ষিপ্ত এবং সহায়ক উত্তর দিন।"""
        else:
            return """You are Jerico, an advanced voice AI assistant. Your job is to understand user commands and perform tasks.
            You can open applications, write code, create files, search the web, and much more.
            Always provide clear, concise responses. Help users accomplish their goals efficiently."""
    
    def handle_command(self, user_input):
        """Parse and handle user command"""
        # Translate Bengali if needed
        language = self.detect_language(user_input)
        
        # Try to parse as command
        command_type, params = CommandHandler.parse_command(user_input)
        
        if command_type:
            result = CommandHandler.execute(command_type, params)
            self.speak(result)
            return
        
        # Fall back to AI processing
        response = self.process_with_ai(user_input)
        self.speak(response, force_language=language)
    
    def interactive_mode(self):
        """Run in interactive text mode (for testing)"""
        print("\n📝 Interactive Mode (Text-based)")
        print("Type your commands or 'quit' to exit:\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                self.speak("Goodbye! See you later!")
                break
            
            self.handle_command(user_input)
    
    def voice_mode(self):
        """Run in voice mode"""
        print("\n🎤 Voice Mode Active")
        print(f"Wake word: '{self.config['wake_word']}'")
        print("Listening for voice commands...\n")
        
        try:
            while True:
                # Listen for wake word
                user_input = self.listen("en-US")
                
                if not user_input:
                    continue
                
                # Check for wake word
                if self.config['wake_word'].lower() not in user_input:
                    continue
                
                # Confirmed activation
                print("✅ Jerico activated!")
                self.speak("I'm listening. What would you like me to do?")
                
                # Get the actual command
                command = self.listen("en-US")
                
                if command:
                    self.handle_command(command)
        
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down Jerico...")
            self.speak("Goodbye! Have a great day!")
    
    def run(self, mode='voice'):
        """Run Jerico"""
        if mode == 'interactive' or mode == 'text':
            self.interactive_mode()
        else:
            self.voice_mode()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Jerico Voice AI Agent')
    parser.add_argument(
        '--mode',
        choices=['voice', 'text', 'interactive'],
        default='voice',
        help='Operation mode (default: voice)'
    )
    
    args = parser.parse_args()
    
    try:
        agent = JericoExtended()
        agent.run(mode=args.mode)
    except KeyboardInterrupt:
        print("\n\n👋 Jerico shutting down...")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
