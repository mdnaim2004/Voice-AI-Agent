import os
import json
import sys
import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import subprocess
import webbrowser
from pathlib import Path
from dotenv import load_dotenv
import threading
from pynput import keyboard

# Load environment variables
load_dotenv()

class JericoAgent:
    def __init__(self):
        """Initialize Jerico Voice AI Agent"""
        self.config = self.load_config()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speech rate
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        self.is_listening = False
        self.current_language = "en"  # Default language
        
        print("🤖 Jerico Voice AI Agent initialized!")
        print(f"Version: {self.config['version']}")
        print(f"Agent Name: {self.config['agent_name']}")
        print("Say 'Jerico' to wake me up, or press 'J' key to activate...")
    
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
            with self.microphone as source:
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
        """Process user command using OpenAI"""
        try:
            # Detect language
            language = self.detect_language(user_input)
            self.current_language = language
            
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
            error_msg = f"Error processing command: {str(e)}"
            print(f"❌ {error_msg}")
            return "Sorry, I encountered an error processing your request."
    
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
        """Main loop for Jerico"""
        print("\n🎯 Jerico is ready! Say 'Jerico' to activate, or press 'J' key...")
        print("Type 'quit' to exit\n")
        
        listener = keyboard.Listener(on_press=self.on_key_press)
        listener.start()
        
        try:
            while True:
                # Listen for command
                user_input = self.listen("en-US")
                
                if not user_input:
                    continue
                
                # Check for wake word
                if not self.wake_word_detection(user_input):
                    continue
                
                print(f"✅ Jerico activated!")
                self.speak("I'm listening. What would you like me to do?")
                
                # Listen for actual command
                command = self.listen("en-US")
                
                if not command:
                    continue
                
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
            listener.stop()
    
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
    agent = JericoAgent()
    agent.run()
