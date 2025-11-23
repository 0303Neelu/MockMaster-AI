MockMaster AI — Voice-enabled Mock Interview Agent

One-line: A voice-first, role-aware mock-interview agent implemented as a single Streamlit app (app.py).
Uses Groq (Whisper + LLaMA) for ASR and LLM, and Edge-TTS (or local alternatives) for speech output.

Table of contents

1. What this repo contains
2. Prerequisites
3. Quick start (recommended)
4. Detailed installation & setup (step-by-step)
5. Environment variables / .env example
6. Run the app locally
7. How the app works (high level)
8. Mermaid architecture diagram
9. Demo guidance / 10-minute script summary
10. Common errors & troubleshooting
11. Security & privacy notes
12. How to publish on GitHub (short)
13. License

1. What this repo contains

  • app.py — Single-file Streamlit app implementing the interview agent.

  • README.md — (this file) Setup, architecture, design & demo guidance.

If you add files later (requirements, demo videos, readme variants), list them in the repository root.

2. Prerequisites

  • Python 3.11 (recommended) — other 3.x might work but 3.11 is tested.

  • pip (Python package manager).

  • ffmpeg installed and available on your PATH — used to convert uploaded audio to 16k mono WAV.

  • A valid Groq API key (for LLM and Whisper requests) — get this from your Groq Console.

  Optional: An Edge-TTS compatible environment (internet required) or a local TTS fallback (pyttsx3) if you prefer offline speech.

3. Quick start (recommended)

• Clone My repo:

    git clone https://github.com/<your-username>/<your-repo>.git
    cd <your-repo>
    
• Create a virtual environment and install:

    python -m venv .venv
    
    # Windows
    .venv\Scripts\activate
    
    # macOS / Linux
    source .venv/bin/activate
    
    pip install -r requirements.txt

