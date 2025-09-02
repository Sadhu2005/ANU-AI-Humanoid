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
# Configuration for DeepSeek API
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

class AdvancedVoiceAssistant:
    def __init__(self):
        try:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 2024.0
            self.recognizer.dynamic_energy_threshold = False
            self.recognizer.pause_threshold = 1.0
            
            # List available microphones
            print("Available microphones:")
            mic_list = sr.Microphone.list_microphone_names()
            for i, mic_name in enumerate(mic_list):
                print(f"{i}: {mic_name}")
            
            # Auto-select microphone
            try:
                self.microphone = sr.Microphone(device_index=2, sample_rate=16000)
                print("Using microphone index 2.")
            except (AssertionError, OSError):
                try:
                    self.microphone = sr.Microphone(device_index=1, sample_rate=16000)
                    print("Using microphone index 1.")
                except (AssertionError, OSError):
                    self.microphone = sr.Microphone(device_index=None, sample_rate=16000)
                    print("Using default microphone.")
                    
            self.audio_queue = queue.Queue()
            self.is_listening = False
            self.is_processing = False
            self.is_speaking = False
            self.conversation_history = deque(maxlen=10) # Stores last 10 user/assistant turns
            self.interrupt_flag = False
            
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
        """Listen to audio in the background and add to queue."""
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
        """Process audio from the queue."""
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
        """Process audio data and convert to text."""
        try:
            text = self.recognizer.recognize_google(audio)
            
            if text.strip():
                print(f"Recognized: {text}")
                if not self.is_speaking:
                    self.analyze_conversation(text)
            else:
                print("Heard silence or unintelligible audio.")
                
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
        except Exception as e:
            print(f"Unexpected error in process_audio: {e}")

    def call_deepseek_api(self):
        """Call the DeepSeek API with the conversation history."""
        if not DEEPSEEK_API_KEY:
            return "I heard you! This is a test response. Please set your DeepSeek API key to use the real AI."
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        }
        
        # Build the message history for the API from the conversation deque
        messages = [{"role": "system", "content": "You are a helpful and concise voice assistant."}]
        for entry in self.conversation_history:
            if entry.startswith("User:"):
                role = "user"
                content = entry.replace("User:", "", 1).strip()
            elif entry.startswith("Assistant:"):
                role = "assistant"
                content = entry.replace("Assistant:", "", 1).strip()
            else:
                continue
            messages.append({"role": role, "content": content})

        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024,
            "top_p": 0.95,
            "stream": False
        }
        
        try:
            response = requests.post(
                DEEPSEEK_API_URL,
                headers=headers,
                data=json.dumps(data),
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("choices"):
                    return result['choices'][0]['message']['content']
                else:
                    print(f"API Error: Unexpected response format: {result}")
                    return "I received an unusual response from the knowledge service."
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
        """Check if the speech is addressed to the assistant."""
        patterns = [
            r"hey (assistant|robot|computer|anu|ai|a\.i\.)",
            r"okay (assistant|robot|computer|anu|ai|a\.i\.)",
            r"^(assistant|robot|computer|anu|ai|a\.i\.)",
            r"hello (assistant|robot|computer|anu|ai|a\.i\.)",
        ]
        text_lower = text.lower()
        for pattern in patterns:
            if re.search(pattern, text_lower):
                print(f"Wake word detected: {pattern}")
                return True
        return False

    def requires_response(self, text):
        """Check if the content requires a response."""
        question_patterns = [
            r"what|how|why|when|where|who|can you|could you|tell me|explain"
        ]
        text_lower = text.lower()
        for pattern in question_patterns:
            if re.search(pattern, text_lower):
                print(f"Question pattern detected: {pattern}")
                return True
        return False

    def analyze_conversation(self, text):
        """Analyze the conversation and determine if/how to respond."""
        self.conversation_history.append(f"User: {text}")
        
        addressed_to_assistant = self.is_addressed_to_assistant(text)
        requires_response_flag = self.requires_response(text)
        
        print(f"Addressed to assistant: {addressed_to_assistant}, Requires response: {requires_response_flag}")
        
        if not addressed_to_assistant and not requires_response_flag:
            print("Conversation noted but no response needed.")
            return
        
        # Generate response using DeepSeek API
        response = self.call_deepseek_api()
        print(f"Assistant: {response}")
        
        self.conversation_history.append(f"Assistant: {response}")
        self.text_to_speech(response)

    def text_to_speech(self, text):
        """Convert text to speech using Windows SAPI."""
        self.is_speaking = True
        print(f"Speaking: {text}")
        try:
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(text)
        except ImportError:
            print("Text-to-speech requires pywin32. Speaking will be simulated.")
            time.sleep(len(text) / 10) # Simulate speech time
        except Exception as e:
            print(f"Error with text-to-speech: {e}")
            time.sleep(len(text) / 10)
        
        self.is_speaking = False

    def run(self):
        """Main method to run the voice assistant."""
        print("Starting advanced voice assistant...")
        print("Speak clearly after calibration is complete.")
        print("Try saying: 'Hey Assistant, what is artificial intelligence?'")
        print("Press Ctrl+C to stop.")
        
        if not self.listen_in_background():
            print("Failed to start listening. Exiting.")
            return
        
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
        print(f"A critical error occurred: {e}")
        print("Please check your microphone connection and permissions.")