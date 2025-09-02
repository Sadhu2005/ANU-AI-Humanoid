markdown
# ANU 6.0 - Artificial Neural Universe 🤖

<p align="center">
<img src="https://via.placeholder.com/600x300/134e4a/f5f5f4?text=ANU+6.0" alt="ANU 6.0 Project Banner">
</p>

<p align="center">
<strong>An AI-powered humanoid robot designed to be a personalized mentor and an intelligent friend for rural students in India.</strong>
<br />
<br />
<img src="https://img.shields.io/badge/Status-In%20Development-blue" alt="Status">
<img src="https://img.shields.io/badge/Python-3.9%2B-blueviolet" alt="Python Version">
<img src="https://img.shields.io/badge/Platform-Raspberry%20Pi%205-orange" alt="Platform">
<img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

## 🎯 Our Mission

To bridge the educational and digital divide for students in rural Karnataka by providing an accessible, engaging, and distraction-free AI learning companion. ANU 6.0 aims to build English fluency, foster confidence, and become a gateway to technology and information for students and their households.

*This project was initiated by the EvoBot Crew at the Coorg Institute of Technology, Ponnampet.*

## 🧐 The Problem

Rural students face significant hurdles in their educational journey:

- **Lack of Conversational Practice**: No environment to practice spoken English, limiting fluency.
- **The Distraction Dilemma**: Mobile phones, while a resource, are a primary source of distraction.
- **Resource Scarcity**: Limited access to personalized, high-quality teaching aids.
- **The Foundational Gap**: A weak foundation in English creates barriers to higher education and careers in technology.

## ✨ Our Solution: ANU 6.0

ANU 6.0 is a 17-DOF humanoid robot that acts as a physical, AI-powered mentor. It provides a focused, interactive, and bilingual (Kannada & English) learning experience, adapting to each student's unique pace and needs. It's a friend to practice with, a teacher to learn from, and a tool that makes advanced technology accessible and fun.

### Key Features

- 🗣️ **Bilingual Conversation**: Fluent in both Kannada and English for natural interaction.
- 🎓 **Personalized Learning Paths**: Assesses student levels and creates custom lesson plans.
- 🤖 **Physical & Engaging**: Performs gestures like waving and hugging to create a strong, friendly bond.
- 🌐 **Hybrid AI Brain**: Functions offline with on-device models and syncs with powerful cloud APIs when online.
- 👀 **Computer Vision**: Uses OpenCV for face recognition and environmental awareness.
- 📵 **Distraction-Free**: A dedicated device for learning, free from the distractions of mobile phones.

## 🚀 Project Architecture

The system follows a modular, three-stage flow:

1. **Perception (Input)**: The robot gathers data using its webcam (visuals), microphone (voice commands), and environmental sensors (proximity, presence).
2. **Processing (The Brain)**: The Raspberry Pi 5 processes this data. It transcribes speech, analyzes images, and uses its hybrid AI core (local models + cloud APIs) to make decisions.
3. **Actuation (Output)**: The brain sends commands to the PCA9685 servo driver to perform physical actions and to the speaker to generate verbal responses.

## 📁 Repository Structure
anu-6.0/
│
├── 🤖 robot_brain/ # All code that runs on the Raspberry Pi
│ ├── main.py # Main application entry point
│ ├── requirements.txt # Python dependencies for the robot
│ ├── .env.example # Example environment variables
│ ├── config/ # Configuration files
│ │ ├── settings.py # Main configuration settings
│ │ └── servo_config.json # Servo calibration data
│ │
│ ├── core/ # Core system modules
│ │ ├── init.py
│ │ ├── state_manager.py # Manages the robot's current state
│ │ └── connectivity_manager.py # Handles online/offline status
│ │
│ ├── modules/ # Individual functionality modules
│ │ ├── init.py
│ │ ├── speech_processing/ # Handles STT and TTS
│ │ │ ├── init.py
│ │ │ ├── speech_recognizer.py
│ │ │ ├── text_to_speech.py
│ │ │ └── voice_processor.py
│ │ │
│ │ ├── ai_core/ # The AI decision-making brain
│ │ │ ├── init.py
│ │ │ ├── gemini_api.py # Gemini API integration
│ │ │ ├── conversation_manager.py
│ │ │ └── response_generator.py
│ │ │
│ │ ├── vision/ # OpenCV and camera functionalities
│ │ │ ├── init.py
│ │ │ ├── camera_controller.py
│ │ │ └── face_recognition.py
│ │ │
│ │ └── motion/ # Controls physical movements
│ │ ├── init.py
│ │ ├── servo_controller.py # Interface with PCA9685 driver
│ │ ├── motion_planner.py
│ │ └── gestures_library.py # Predefined gestures and actions
│ │
│ ├── utils/ # Utility functions and helpers
│ │ ├── init.py
│ │ ├── logger.py # Logging configuration
│ │ ├── helpers.py # Common helper functions
│ │ └── audio_utils.py # Audio processing utilities
│ │
│ └── tests/ # Unit and integration tests
│ ├── init.py
│ ├── test_speech.py
│ ├── test_vision.py
│ └── test_motion.py
│
├── 🌐 server/ # (Optional) Backend server code
│ ├── main.py
│ ├── requirements.txt
│ └── api/ # API endpoints
│ ├── init.py
│ └── routes.py
│
├── 🛠️ hardware/ # Hardware schematics and documentation
│ ├── ANU_6.0_BOM.csv # Bill of Materials
│ ├── wiring_diagram.png
│ ├── assembly_guide.md
│ └── 3d_models/ # STL files for 3D printed parts
│ ├── head.stl
│ ├── arm.stl
│ └── torso.stl
│
├── 📚 docs/ # Project documentation
│ ├── architecture.md
│ ├── setup_guide.md
│ ├── api_reference.md
│ └── contribution_guide.md
│
├── 📦 datasets/ # Training data and models
│ ├── voice_samples/ # Voice command samples
│ ├── face_data/ # Face recognition training data
│ └── models/ # Pre-trained models
│ ├── vosk-model/ # Offline speech recognition model
│ └── face_recognition_model/
│
├── scripts/ # Deployment and maintenance scripts
│ ├── install_dependencies.sh
│ ├── setup_raspberrypi.sh
│ └── update_robot.sh
│
├── .gitignore
├── LICENSE
├── CODE_OF_CONDUCT.md
└── README.md

text

## ⚙️ Getting Started

### Prerequisites

- Raspberry Pi 5 (8GB RAM recommended) with Raspberry Pi OS (64-bit)
- Python 3.9 or newer
- All hardware components (servos, drivers, camera, microphone, etc.)
- Internet connection (for initial setup)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/anu-6.0.git
   cd anu-6.0/robot_brain
Create a virtual environment:

bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
Set up environment variables:

bash
cp .env.example .env
# Edit .env with your API keys and configuration
Hardware setup:

Follow the hardware assembly guide in /hardware/assembly_guide.md

Connect all servos to the PCA9685 controller

Connect camera and microphone to Raspberry Pi

Configuration
Edit the .env file with your specific configuration:

env
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# Speech Recognition
SPEECH_RECOGNITION_ENGINE=google  # google or vosk
VOSK_MODEL_PATH=./datasets/models/vosk-model

# Text-to-Speech
TTS_ENGINE=pyttsx3  # pyttsx3, gtts, or espeak

# Camera Settings
CAMERA_RESOLUTION=640x480
CAMERA_FPS=30

# Servo Configuration
SERVO_FREQUENCY=50
SERVO_MIN_PULSE=500
SERVO_MAX_PULSE=2500
Running the Robot
bash
# Activate virtual environment
source .venv/bin/activate

# Run the main application
python main.py

# Or run with specific modules
python -m modules.speech_processing.voice_processor
🧪 Testing
Run the test suite to verify all components are working:

bash
# Run all tests
python -m pytest tests/

# Run specific test modules
python -m pytest tests/test_speech.py -v
python -m pytest tests/test_vision.py -v
python -m pytest tests/test_motion.py -v
🤝 Contributing
We welcome contributions! Please read our Contribution Guide for details on our code of conduct and the process for submitting pull requests.

Development Setup
Fork the repository

Create a feature branch: git checkout -b feature/amazing-feature

Commit your changes: git commit -m 'Add amazing feature'

Push to the branch: git push origin feature/amazing-feature

Open a pull request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Coorg Institute of Technology, Ponnampet

EvoBot Crew team members

Open source communities for various libraries and tools

Raspberry Pi Foundation for hardware support

📞 Contact
For questions or support, please contact:

Project Lead: [Your Name] - [your.email@example.com]

Development Team: [team.email@example.com]

🔗 Useful Links
Project Wiki

Issue Tracker

Release Notes

<p align="center"> Made with ❤️ by the EvoBot Crew | Coorg Institute of Technology </p> ```