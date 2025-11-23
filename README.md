MockMaster AI — Voice-enabled Mock Interview Agent

One-line: A voice-first, role-aware mock-interview agent implemented as a single Streamlit app (app.py).
Uses Groq (Whisper + LLaMA) for ASR and LLM, and Edge-TTS (or local alternatives) for speech output.

Table of Contents:

1. Project overview
2. What’s included
3. Prerequisites
4. Quick setup (recommended)
5. Platform-specific setup notes
6. Environment variables
7. Run the app
8. How it works (short walkthrough)
9. Architecture (Mermaid)
10. Design decisions
11. Demo / Recording guide (10 minutes)
12. Troubleshooting
13. Security & privacy notes
14. Extending the project
15. License


1. Project overview

app.py implements a mock interview agent that:

  • Accepts voice answers (via browser upload / mic when supported),
  • Converts audio to 16 kHz mono WAV using FFmpeg,
  • Uses Groq Whisper for speech-to-text,
  • Uses a Groq-hosted LLaMA-based model for question generation, follow-ups and feedback,
  • Uses Edge-TTS (or another local/free TTS) to synthesize spoken questions/answers,
  • Maintains session state to run multi-turn interviews and produce structured final feedback.

This single-file project is intentionally minimal to make setup and demonstration fast.

2. Whats included

  • app.py — the complete Streamlit application (UI, audio helpers, LLM calls, TTS glue).

  • README.md — this file (setup, run, architecture, demo guidance).

3. Prerequisites

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
    
• Install Python dependencies:

    pip install streamlit groq edge-tts ffmpeg-python soundfile numpy

• Ensure FFmpeg is installed and on PATH

  • macOS: 
      
      brew install ffmpeg (if you use Homebrew)

  • Ubuntu/Debian:
  
      sudo apt update && sudo apt install ffmpeg -y

  • Windows: download a build from https://www.gyan.dev/ffmpeg/builds/ and add ffmpeg/bin to your PATH

• Set environment variables
    Create a .env file or export variables directly. At minimum you must provide your Groq API key:

  • Example .env file (do not commit this to git):
  
      GROQ_API_KEY=gsk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

• To load env in your terminal (temporary):

  • macOS / Linux:

      export GROQ_API_KEY="gsk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


  • Windows (PowerShell):

    $env:GROQ_API_KEY="gsk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


(If app.py expects other keys — e.g., OpenAI — set them similarly.)

5. Platform-specific setup notes

  • Windows: Install FFmpeg and ensure ffmpeg.exe is on PATH; restart terminals after adding to PATH. If edge-tts fails in certain environments, you can try pyttsx3 as an offline fallback.

  • Colab: Browser mic recording is limited; prefer uploading audio files or run locally.

  • Linux: Make sure the user running Streamlit has permission to run FFmpeg and write temp files.

6. Environment variables

  • The app reads environment variables for API keys. Typical names used in app.py:

  • GROQ_API_KEY — required for Groq LLM and Whisper calls.

  • If you change keys or providers in app.py, update the README and .env accordingly.

7. Run the app

  Run Streamlit locally from project folder:

    # Make sure virtual env is activated and env vars are set
    streamlit run app.py


  Open the URL printed by Streamlit (usually http://localhost:8501) in your browser.

8. How it works (short walkthrough)

  1. Choose the role (Software Engineer, Sales, etc.) from the dropdown.
  2. Click Start Interview — the app generates and displays the first question.
  3. Record or upload your spoken answer using the audio input widget.
  4. The app converts audio → 16 kHz WAV (FFmpeg), sends to Groq Whisper, receives transcript.
  5. Transcript is appended to session history and passed to the LLM to create the next question or handle follow-up mode.
  6. After the interview ends, a final structured feedback is generated and displayed.
