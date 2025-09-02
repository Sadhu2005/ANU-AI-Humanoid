# test_mic.py
import speech_recognition as sr
import time

def test_microphone():
    r = sr.Recognizer()
    
    # List available microphones
    print("Available microphones:")
    mics = sr.Microphone.list_microphone_names()
    for i, mic in enumerate(mics):
        print(f"{i}: {mic}")
    
    # Try to use a microphone
    try:
        # Try the Realtek microphone (index 1 from your list)
        with sr.Microphone(device_index=1) as source:
            print("Calibrating for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=2)
            print(f"Energy threshold: {r.energy_threshold}")
            
            print("Please say something...")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Got audio, processing...")
            
            try:
                text = r.recognize_google(audio)
                print(f"You said: {text}")
                return True
            except sr.UnknownValueError:
                print("Could not understand audio")
                return False
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
                return False
                
    except Exception as e:
        print(f"Microphone error: {e}")
        return False

if __name__ == "__main__":
    if test_microphone():
        print("Microphone test passed!")
    else:
        print("Microphone test failed!")