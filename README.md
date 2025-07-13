# Voice Assistant

A modular voice assistant that responds to voice commands using OpenAI's Whisper for speech recognition.

## Features

- Voice recording and transcription
- Modular command system
- Activation word detection
- Extensible architecture

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

3. Run the assistant:
```bash
python -m src.main
```

## Usage

- Press Enter to start recording
- Say the activation word ("furina" or "purina") followed by your command
- The assistant will process and respond to your command

## Project Structure

```
src/
├── audio/
│   ├── recorder.py      # Audio recording functionality
│   └── transcriber.py   # Speech-to-text transcription
├── commands/
│   └── base.py          # Base command system
└── main.py              # Main application
```

## Development

This project uses feature branches for development:
- `feature/command-system` - Core command architecture
- `feature/additional-commands` - Basic commands implementation
- `feature/text-to-speech` - Voice responses
- `feature/improved-detection` - Better command detection