import streamlit as st
import tempfile
import os
import ffmpeg
from groq import Groq


# Initialize Groq Client
client = Groq(api_key="YOUR_API_KEY")

LLM_MODEL = "llama-3.3-70b-versatile"
ASR_MODEL = "whisper-large-v3"

# Page UI config
st.set_page_config(page_title="AI Mock Interview Agent", layout="centered")

st.title("AI Mock Interview Practice Agent")

# Role Selection
role = st.selectbox(
    "Select Interview Role",
    ["Software Engineer", "Sales Associate", "Retail Associate", "Data Analyst", "Product Manager"]
)


# Session State
if "history" not in st.session_state:
    st.session_state.history = []

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "interview_over" not in st.session_state:
    st.session_state.interview_over = False

if "followup_mode" not in st.session_state:
    st.session_state.followup_mode = False

if "question_count" not in st.session_state:
    st.session_state.question_count = 0


# Convert uploaded audio → WAV
def convert_audio_to_wav(file_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp_in:
        tmp_in.write(file_bytes)
        tmp_in.flush()
        input_path = tmp_in.name

    output_path = input_path.replace(".webm", "_16k.wav")

    (
        ffmpeg
        .input(input_path)
        .output(output_path, ar=16000, ac=1)
        .run(quiet=True, overwrite_output=True)
    )
    return output_path


# STT: English output
def transcribe_audio(path):
    with open(path, "rb") as f:
        resp = client.audio.transcriptions.create(
            file=(os.path.basename(path), f.read()),
            model=ASR_MODEL,
            response_format="verbose_json",
            language="en"
        )
    return resp.text

# Ask next interview question
def llm_next_question(role, history):
    messages = [{"role": "system", "content": f"You are a professional interviewer for a {role} job role."}]
    
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["text"]})

    messages.append({"role": "user", "content": "Ask the next interview question."})

    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        max_tokens=300
    )
    return resp.choices[0].message.content

# ---------------------------------------------------------
# Ask follow-up question
# ---------------------------------------------------------
def llm_followup(role, user_question):
    messages = [
        {"role": "system", "content": f"You are the interviewer finishing a {role} interview."},
        {"role": "user", "content": user_question},
    ]

    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        max_tokens=200
    )
    return resp.choices[0].message.content

# Final Feedback
def generate_feedback(role, history):
    messages = [
        {"role": "system", "content": "You are an HR interviewer and evaluator."},
        {"role": "user",
         "content": f"""Provide structured final feedback for this {role} interview.

Conversation history:
{history}

Sections:
1. Summary
2. Communication strengths/weaknesses
3. Technical evaluation
4. Confidence / presence
5. Suggestions to improve
6. Score out of 10 with justification
"""
         }
    ]

    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        max_tokens=600
    )
    return resp.choices[0].message.content


# START INTERVIEW
if st.session_state.current_question is None and not st.session_state.interview_over:
    if st.button("Start Interview"):
        seed_prompt = [
            {"role": "system", "content": f"You are a professional interviewer for a {role} role."},
            {"role": "user", "content": "Ask the first interview question."},
        ]
        resp = client.chat.completions.create(model=LLM_MODEL, messages=seed_prompt, max_tokens=200)
        first_q = resp.choices[0].message.content

        st.session_state.current_question = first_q
        st.session_state.history.append({"role": "assistant", "text": first_q})
        st.rerun()

# MAIN INTERVIEW LOOP
if st.session_state.current_question and not st.session_state.interview_over and not st.session_state.followup_mode:

    st.subheader("Interview Question:")
    st.write(st.session_state.current_question)

    audio_uploaded = st.audio_input("Record your voice answer", key=f"audio_{st.session_state.question_count}")

    st.write("OR click below to end the interview anytime:")
    if st.button("End Interview Now"):
        st.session_state.followup_mode = True  # Move to follow-up mode
        st.rerun()

    if audio_uploaded:
        transcript = transcribe_audio(convert_audio_to_wav(audio_uploaded.getvalue()))

        st.session_state.history.append({"role": "user", "text": transcript})

        if transcript.lower().strip() in ["exit", "quit", "stop", "end"]:
            st.session_state.followup_mode = True
            st.rerun()

        st.session_state.question_count += 1

        if st.session_state.question_count >= 7:
            st.session_state.history.append({"role": "assistant", "text": "Before we conclude, do you have any questions for me?"})
            st.session_state.followup_mode = True
            st.rerun()

        next_q = llm_next_question(role, st.session_state.history)
        st.session_state.history.append({"role": "assistant", "text": next_q})
        st.session_state.current_question = next_q
        st.rerun()

# FOLLOW-UP QUESTION LOOP (UPDATED)
if st.session_state.followup_mode and not st.session_state.interview_over:
    st.subheader("Follow-Up Questions Round")
    st.write("You can ask questions to the interviewer. Say **stop / end / no** to finish.")

    audio_follow = st.audio_input("Record your follow-up question 👇", key=f"follow_{st.session_state.question_count}")

    if audio_follow:
        transcript = transcribe_audio(convert_audio_to_wav(audio_follow.getvalue()))
        st.write("You asked:", transcript)

        stop_words = ["no", "nothing", "no questions", "stop", "end", "exit", "quit"]

        clean_text = transcript.lower().strip()

        # partial match instead of exact match
        if any(word in clean_text for word in stop_words):
            st.session_state.interview_over = True
            st.rerun()

        # If not ending, interviewer answers
        answer = llm_followup(role, transcript)
        st.session_state.history.append({"role": "assistant", "text": answer})

        st.write("Interviewer:", answer)


# FINAL FEEDBACK
if st.session_state.interview_over:
    st.subheader("Interview Completed!")
    st.write("Generating feedback...")

    feedback = generate_feedback(role, st.session_state.history)
    st.text_area("Final Feedback", feedback, height=350)

    if st.button("Restart Interview"):
        st.session_state.history = []
        st.session_state.current_question = None
        st.session_state.interview_over = False
        st.session_state.followup_mode = False
        st.session_state.question_count = 0
        st.rerun()
