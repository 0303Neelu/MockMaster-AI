AI INTERVIEWER AGENT
====================

This project implements a lightweight AI-powered voice-based Interview Agent.
It asks interview questions, listens to your recorded answers, generates follow-up
questions, and continues until you say a stop command.

The system runs locally using Streamlit and Groq LLMs for question generation
and speech-to-text processing.

---------------------------------------------------------------------

FEATURES
--------

• Voice-based interview interaction  
• Converts speech → text → AI response  
• Multi-role interview support  
• Continuous interview questioning  
• Simple Streamlit user interface  
• Single-file architecture (app.py)

---------------------------------------------------------------------

INSTALLATION AND SETUP
----------------------

1. Clone the Repository
-----------------------

    git clone https://github.com/<your-username>/<repo-name>.git
    cd <repo-name>

2. Create a Virtual Environment (Recommended)
---------------------------------------------
    python -m venv venv
    
    Activate the environment:
    
    Windows:
        venv\Scripts\activate
    
    Mac / Linux:
        source venv/bin/activate

3. Install Dependencies
-----------------------
    If a requirements.txt file exists:
        pip install -r requirements.txt
    
    OR install manually:
        pip install streamlit groq ffmpeg-python
    
    Note: You must have FFmpeg installed on your computer.

4. Set Your API Key
-------------------
Create a .env file and add:

    GROQ_API_KEY=your_api_key_here

Or set it manually:

    Windows:
        set GROQ_API_KEY=your_api_key_here
    
    Mac / Linux:
        export GROQ_API_KEY=your_api_key_here

---------------------------------------------------------------------

RUNNING THE APPLICATION
-----------------------
Start the Streamlit application with:

    streamlit run app.py

This will automatically open the interface in your browser.

---------------------------------------------------------------------

ARCHITECTURE OVERVIEW
---------------------

High-Level Workflow:
--------------------
User Speech → Audio Upload → FFmpeg Conversion → Whisper ASR (Groq)
→ LLaMA 3.3 Interview Logic → Streamlit UI → Loop

Architecture Diagram:
--------------------------------------

<img width="1717" height="962" alt="Mock Interview Agent" src="https://github.com/user-attachments/assets/8e4800a4-e4ca-4531-abd4-b4e3f374e211" />

---------------------------------------------------------------------

SUPPORTED INTERVIEW ROLES
-------------------------

• Software Engineer
• Data Analyst
• Product Manager
• Sales Associate
• Retail Associate

---------------------------------------------------------------------

PROJECT STRUCTURE
-----------------
app.py        - Main application file  
README.txt    - Documentation  

---------------------------------------------------------------------

DESIGN DECISIONS
----------------

• Built as a single-file agent for simplicity and clarity.  
• Uses Groq Whisper for fast and accurate speech recognition.  
• Uses Groq LLaMA 3.3 model for dynamic interview question generation.  
• Streamlit chosen for rapid prototyping and easy voice-recording UI.  
• Session state maintains interview flow, history, and role selection.

---------------------------------------------------------------------

LICENSE
-------
This project is released under the MIT License.

---------------------------------------------------------------------

