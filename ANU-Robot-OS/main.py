# main.py
try:
    import speech_recognition as sr
    import threading
    import queue
    import time
    import requests
    import json
    import re
    import os
    import sys
    from collections import deque
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Please install required packages using: pip install SpeechRecognition pyaudio requests pywin32")
    sys.exit(1)

load_dotenv()
# Configuration
GEMINI_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GEMINI_API_URL = "https://api.deepseek.com/v1/chat/completions"

class AdvancedVoiceAssistant:
    def __init__(self):
        try:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 2024.0  # Use your calibrated value
            self.recognizer.dynamic_energy_threshold = False
            self.recognizer.pause_threshold = 1.0
            
            # List available microphones
            print("Available microphones:")
            mic_list = sr.Microphone.list_microphone_names()
            for i, mic_name in enumerate(mic_list):
                print(f"{i}: {mic_name}")
            
            # Try different microphones - let's try your headset (index 2)
            try:
                self.microphone = sr.Microphone(device_index=2, sample_rate=16000)
                print("Using microphone index 2: Headset (Mivi SuperPods Halo)")
            except:
                try:
                    self.microphone = sr.Microphone(device_index=1, sample_rate=16000)
                    print("Using microphone index 1: Realtek Audio")
                except:
                    self.microphone = sr.Microphone(device_index=None, sample_rate=16000)
                    print("Using default microphone")
                
            self.audio_queue = queue.Queue()
            self.is_listening = False
            self.is_processing = False
            self.is_speaking = False
            self.conversation_history = deque(maxlen=10)
            self.interrupt_flag = False
            self.participants = set()
            
            # Adjust for ambient noise
            print("Calibrating for ambient noise. Please wait...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print(f"Energy threshold set to: {self.recognizer.energy_threshold}")
            print("Voice assistant initialized successfully.")
            
        except Exception as e:
            print(f"Failed to initialize voice assistant: {e}")
            raise
    
    def listen_in_background(self):
        """Listen to audio in the background and add to queue"""
        def callback(recognizer, audio):
            if self.is_listening and not self.is_processing and not self.is_speaking:
                self.audio_queue.put(audio)
        
        self.is_listening = True
        try:
            self.stop_listening = self.recognizer.listen_in_background(
                self.microphone, 
                callback, 
                phrase_time_limit=5
            )
            print("Started listening in background...")
            return True
        except Exception as e:
            print(f"Error starting background listener: {e}")
            self.is_listening = False
            return False
    
    def process_audio_queue(self):
        """Process audio from the queue"""
        while self.is_listening:
            try:
                audio = self.audio_queue.get(timeout=1)
                if audio:
                    self.is_processing = True
                    self.process_audio(audio)
                    self.is_processing = False
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing audio queue: {e}")
                self.is_processing = False
    
    def process_audio(self, audio):
        """Process audio data and convert to text"""
        try:
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            
            if text.strip():
                print(f"Recognized: {text}")
                
                # Check if this is a new speaker
                if not self.is_speaking:
                    self.analyze_conversation(text)
            else:
                print("Heard silence or unintelligible audio")
                
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
        except Exception as e:
            print(f"Unexpected error in process_audio: {e}")
    
    def call_gemini_api(self, prompt, context=""):
        """Call the Gemini API with the given prompt and context"""
        # If no API key is set, use a mock response for testing
        if GEMINI_API_KEY == "your_gemini_api_key_here":
            return "I heard you! This is a test response. Please set your Gemini API key to use the real AI."
        
        headers = {
            "Content-Type": "application/json",
        }
        
        full_prompt = f"{context}\n\nCurrent input: {prompt}"
        
        data = {
            "contents": [{
                "parts": [{
                    "text": full_prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }
        
        try:
            response = requests.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                headers=headers,
                data=json.dumps(data),
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"API Error: {response.status_code}, {response.text}")
                return "I'm having trouble connecting to the knowledge service."
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return "I'm experiencing network issues. Please try again later."
        except Exception as e:
            print(f"Unexpected error in API call: {e}")
            return "Sorry, I encountered an unexpected error."
    
    def is_addressed_to_assistant(self, text):
        """Check if the speech is addressed to the assistant"""
        patterns = [
            r"hey (assistant|robot|computer|anu|ai|a\.i\.)",
            r"okay (assistant|robot|computer|anu|ai|a\.i\.)",
            r"^(assistant|robot|computer|anu|ai|a\.i\.)",
            r"hello (assistant|robot|computer|anu|ai|a\.i\.)",
            r"okay (google|alexa|siri|cortana)",
            r"hey (google|alexa|siri|cortana)",
            r"^listen",
            r"^attention",
            r"wake up",
            r"are you there",
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            if re.search(pattern, text_lower):
                print(f"Wake word detected: {pattern}")
                return True
        return False
    
    def requires_response(self, text):
        """Check if the content requires a response"""
        question_patterns = [
            r"what(\s+is|\s+are|\s+do|\s+does|\s+did|\s+will|\s+would|\s+could|\s+should|\s+can|\s+'s)?\s+.*\?",
            r"how(\s+is|\s+are|\s+do|\s+does|\s+did|\s+will|\s+would|\s+could|\s+should|\s+can)?\s+.*\?",
            r"why(\s+is|\s+are|\s+do|\s+does|\s+did|\s+will|\s+would|\s+could|\s+should|\s+can)?\s+.*\?",
            r"when(\s+is|\s+are|\s+do|\s+does|\s+did|\s+will|\s+would|\s+could|\s+should|\s+can)?\s+.*\?",
            r"where(\s+is|\s+are|\s+do|\s+does|\s+did|\s+will|\s+would|\s+could|\s+should|\s+can)?\s+.*\?",
            r"who(\s+is|\s+are|\s+do|\s+does|\s+did|\s+will|\s+would|\s+could|\s+should|\s+can)?\s+.*\?",
            r"can you.*\?",
            r"could you.*\?",
            r"would you.*\?",
            r"should I.*\?",
            r"is it.*\?",
            r"are you.*\?",
            r"do you.*\?",
            r"will you.*\?",
            r"tell me about",
            r"explain to me",
            r"give me information about",
            r"what's your opinion on",
            r"i need help with",
        ]
        
        text_lower = text.lower()
        for pattern in question_patterns:
            if re.search(pattern, text_lower):
                print(f"Question detected: {pattern}")
                return True
        return False
    
    def analyze_conversation(self, text):
        """Analyze the conversation and determine if/how to respond"""
        # Add to conversation history
        self.conversation_history.append(f"User: {text}")
        
        # Check if the assistant is being addressed directly
        addressed_to_assistant = self.is_addressed_to_assistant(text)
        
        # Check if this requires an immediate response
        requires_response = self.requires_response(text)
        
        print(f"Addressed to assistant: {addressed_to_assistant}, Requires response: {requires_response}")
        
        # If not specifically addressed and doesn't require response, just listen
        if not addressed_to_assistant and not requires_response:
            print("Conversation noted but no response needed.")
            return
        
        # Get context from conversation history
        context = "\n".join(self.conversation_history)
        
        # Generate response using Gemini API
        response = self.call_gemini_api(text, context)
        print(f"Assistant: {response}")
        
        # Add assistant response to history
        self.conversation_history.append(f"Assistant: {response}")
        
        # Convert response to speech
        self.text_to_speech(response)
    
    def text_to_speech(self, text):
        """Convert text to speech using Windows SAPI"""
        self.is_speaking = True
        print(f"Speaking: {text}")
        
        # Use Windows built-in text-to-speech
        try:
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            # Rate of speech (-10 to 10, 0 is normal)
            speaker.Rate = 0
            # Volume (0 to 100)
            speaker.Volume = 100
            speaker.Speak(text)
        except ImportError:
            print("Text-to-speech requires pywin32 package. Install with: pip install pywin32")
            # Fallback: just print the text
            time.sleep(len(text) / 10)
        except Exception as e:
            print(f"Error with text-to-speech: {e}")
            time.sleep(len(text) / 10)
        
        self.is_speaking = False
    
    def run(self):
        """Main method to run the voice assistant"""
        print("Starting advanced voice assistant...")
        print("Speak clearly into the microphone after the calibration is complete.")
        print("Try saying: 'Hey Assistant, what is artificial intelligence?'")
        print("Or: 'What is the weather today?'")
        print("Press Ctrl+C to stop the assistant.")
        
        # Start listening in background
        success = self.listen_in_background()
        
        if not success:
            print("Failed to start listening. Exiting.")
            return
        
        # Start processing thread
        processing_thread = threading.Thread(target=self.process_audio_queue)
        processing_thread.daemon = True
        processing_thread.start()
        
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nStopping voice assistant...")
            self.is_listening = False
            if hasattr(self, 'stop_listening'):
                self.stop_listening(wait_for_stop=False)
            print("Voice assistant stopped.")

if __name__ == "__main__":
    try:
        assistant = AdvancedVoiceAssistant()
        assistant.run()
    except Exception as e:
        print(f"Failed to initialize voice assistant: {e}")
        print("Please check your microphone connection and permissions.")