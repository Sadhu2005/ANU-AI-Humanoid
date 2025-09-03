import threading
import queue
import json
import pyaudio
import vosk
from silero_vad import load_silero_vad, apply_silero_vad
from utils.tts import TextToSpeech

class SpeechProcessor:
    def __init__(self, output_queue, config):
        self.output_queue = output_queue
        self.config = config
        self.running = False
        self.audio = pyaudio.PyAudio()
        
        # Initialize Vosk model
        self.vosk_model = vosk.Model(self.config.VOSK_MODEL_PATH)
        
        # Initialize Silero VAD
        self.vad_model = load_silero_vad(self.config.SILERO_VAD_PATH)
        
        # Initialize TTS
        self.tts_engine = TextToSpeech()
        
        # Audio settings
        self.rate = 16000
        self.chunk_size = 8000
        
    def run(self):
        """Run speech processing in a separate thread"""
        self.running = True
        
        # Start audio stream
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        rec = vosk.KaldiRecognizer(self.vosk_model, self.rate)
        
        print("Speech processor started. Listening...")
        while self.running:
            data = stream.read(self.chunk_size, exception_on_overflow=False)
            
            # Check if speech is detected using VAD
            if apply_silero_vad(self.vad_model, data):
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if result['text']:
                        # Add to output queue
                        self.output_queue.put({
                            'type': 'speech',
                            'text': result['text'],
                            'confidence': result.get('confidence', 0.5)
                        })
        
        stream.stop_stream()
        stream.close()
    
    def speak(self, text):
        """Convert text to speech"""
        self.tts_engine.speak(text)
    
    def stop(self):
        """Stop speech processing"""
        self.running = False
        self.audio.terminate()