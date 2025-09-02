# ANU-
Artificial Neural Univers   
ANU 6.0 - Artificial Neural Universe 🤖
<p align="center">
<img src="https://www.google.com/search?q=https://placehold.co/600x300/134e4a/f5f5f4%3Ftext%3DANU%2B6.0%26font%3Dinter" alt="ANU 6.0 Project Banner">
</p>

<p align="center">
<strong>An AI-powered humanoid robot designed to be a personalized mentor and an intelligent friend for rural students in India.</strong>
<br />
<br />
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Status-In%2520Development-blue" alt="Status">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Python-3.9%252B-blueviolet" alt="Python Version">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Platform-Raspberry%2520Pi%25205-orange" alt="Platform">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

🎯 Our Mission
To bridge the educational and digital divide for students in rural Karnataka by providing an accessible, engaging, and distraction-free AI learning companion. ANU 6.0 aims to build English fluency, foster confidence, and become a gateway to technology and information for students and their households.

This project was initiated by the EvoBot Crew at the Coorg Institute of Technology, Ponnampet.

🧐 The Problem
Rural students face significant hurdles in their educational journey:

Lack of Conversational Practice: No environment to practice spoken English, limiting fluency.

The Distraction Dilemma: Mobile phones, while a resource, are a primary source of distraction.

Resource Scarcity: Limited access to personalized, high-quality teaching aids.

The Foundational Gap: A weak foundation in English creates barriers to higher education and careers in technology.

✨ Our Solution: ANU 6.0
ANU 6.0 is a 17-DOF humanoid robot that acts as a physical, AI-powered mentor. It provides a focused, interactive, and bilingual (Kannada & English) learning experience, adapting to each student's unique pace and needs. It's a friend to practice with, a teacher to learn from, and a tool that makes advanced technology accessible and fun.

Key Features
🗣️ Bilingual Conversation: Fluent in both Kannada and English for natural interaction.

🎓 Personalized Learning Paths: Assesses student levels and creates custom lesson plans.

🤖 Physical & Engaging: Performs gestures like waving and hugging to create a strong, friendly bond.

🌐 Hybrid AI Brain: Functions offline with on-device models and syncs with powerful cloud APIs when online.

👀 Computer Vision: Uses OpenCV for face recognition and environmental awareness.

📵 Distraction-Free: A dedicated device for learning, free from the distractions of mobile phones.

🚀 Project Architecture
The system follows a modular, three-stage flow:

Perception (Input): The robot gathers data using its webcam (visuals), microphone (voice commands), and environmental sensors (proximity, presence).

Processing (The Brain): The Raspberry Pi 5 processes this data. It transcribes speech, analyzes images, and uses its hybrid AI core (local models + cloud APIs) to make decisions.

Actuation (Output): The brain sends commands to the PCA9685 servo driver to perform physical actions and to the speaker to generate verbal responses.

📁 Directory Structure
The repository is organized to separate concerns, making development and maintenance clean and scalable.

anu-6.0/
│
├── 🤖 robot_brain/                # All code that runs on the Raspberry Pi
│   ├── main.py                     # Main application entry point
│   ├── requirements.txt            # Python dependencies for the robot
│   ├── .env.example                # Example environment variables
│   │
│   ├── core/                       # Core system modules
│   │   ├── __init__.py
│   │   ├── state_manager.py        # Manages the robot's current state (e.g., listening, speaking, moving)
│   │   └── connectivity_manager.py # Handles online/offline status and server communication
│   │
│   ├── modules/                    # Individual functionality modules
│   │   ├── __init__.py
│   │   ├── speech_processing/      # Handles STT and TTS
│   │   │   ├── __init__.py
│   │   │   ├── offline_stt.py      # Vosk for local speech-to-text
│   │   │   └── online_tts.py       # Google/API-based text-to-speech
│   │   │
│   │   ├── ai_core/                # The AI decision-making brain
│   │   │   ├── __init__.py
│   │   │   ├── offline_llm.py      # Small, local LLM for offline responses
│   │   │   └── online_llm_api.py   # Handles API calls to Gemini, etc.
│   │   │
│   │   ├── vision/                 # OpenCV and camera functionalities
│   │   │   ├── __init__.py
│   │   │   └── face_recognition.py
│   │   │
│   │   └── motion/                 # Controls physical movements
│   │       ├── __init__.py
│   │       ├── servo_control.py    # Interface with PCA9685 driver
│   │       └── actions.py          # Defines complex actions (hug, wave, dance)
│   │
│   └── logs/                       # For storing runtime logs
│       └── robot.log
│
├── 🌐 server/                     # (Optional) Backend server code for online mode
│   ├── main.py
│   └── requirements.txt
│
├── 🛠️ hardware/                    # Hardware schematics, wiring diagrams, and parts list
│   ├── ANU_6.0_BOM.csv             # Bill of Materials
│   └── wiring_diagram.png
│
├── 📚 docs/                        # Project documentation
│   ├── architecture.md
│   └── setup_guide.md
│
├── .gitignore
└── README.md

⚙️ Getting Started (Robot Setup)
These instructions will get a copy of the robot's brain running on your Raspberry Pi 5.

Prerequisites
Raspberry Pi 5 (8GB RAM recommended) with Raspberry Pi OS (64-bit).

Python 3.9 or newer.

All hardware components (servos, drivers, camera, etc.) connected.

Internet connection (for initial setup).

Installation
Clone the repository:

git clone [https://github.com/your-username/anu-6.0.git](https://github.com/your-username/anu-6.0.git)
cd anu-6.0/robot_brain

Create a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Set up environment variables:

Copy the example file:

cp .env.example .env

Edit the .env file and add your API keys for online services (like Gemini).

# .env
GEMINI_API_KEY="YOUR_API_KEY_HERE"

Running the Robot
Execute the main script:

python main.py
