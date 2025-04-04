import streamlit as st
import whisper
import sounddevice as sd
import tempfile
import os
import scipy.io.wavfile
from gpt4all import GPT4All

# --- CONFIG ---
MODEL_PATH = "./models/ggml-gpt4all-j-v1.3-groovy.bin"
RECORD_DURATION = 5  # seconds
SAMPLE_RATE = 44100  # Hz

# --- Load Whisper ---
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

# --- Load GPT4All with Error Handling ---
@st.cache_resource
def load_gpt4all_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"❌ GPT4All model not found at: {MODEL_PATH}")
        st.stop()
    return GPT4All("ggml-gpt4all-j", model_path=MODEL_PATH)

# --- Load Models ---
whisper_model = load_whisper_model()
gpt4all_model = load_gpt4all_model()

# --- Streamlit UI ---
st.set_page_config(page_title="Talk2Code (Offline)", layout="centered")
st.title("🎤 Talk2Code (Offline)")
st.markdown("Record your voice or upload audio → Get Python code (offline, open-source)")

# --- Audio Path Initialization ---
audio_path = None

# --- Choose Input Method ---
option = st.radio("🎛️ Choose input method:", ["🎙️ Record from mic", "📁 Upload audio file"])

# --- Handle Input ---
if option == "🎙️ Record from mic":
    st.info("Press the button to start recording your voice...")

    if st.button("🎤 Start Recording"):
        st.success("🔴 Recording... Speak now!")
        recording = sd.rec(int(RECORD_DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
        sd.wait()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            scipy.io.wavfile.write(tmp.name, SAMPLE_RATE, recording)
            audio_path = tmp.name
            st.audio(tmp.name, format="audio/wav")

elif option == "📁 Upload audio file":
    audio_file = st.file_uploader("📤 Upload audio (.mp3, .wav, .m4a)", type=["mp3", "wav", "m4a"])
    if audio_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(audio_file.read())
            audio_path = tmp.name
        st.audio(audio_file)

# --- Transcribe & Generate Code ---
if audio_path:
    with st.spinner("🔍 Transcribing..."):
        result = whisper_model.transcribe(audio_path)
        prompt = result["text"].strip()

    st.success("📝 Transcribed Text:")
    st.write(f"**{prompt}**")

    with st.spinner("🛠️ Generating Code..."):
        instruction = f"Write a Python script for: {prompt}"
        response = gpt4all_model.generate(instruction, max_tokens=300)

    st.success("✅ Generated Code:")
    st.code(response, language="python")

    # --- Save Code as .py ---
    st.download_button("💾 Download Code as .py", data=response, file_name="generated_code.py", mime="text/x-python")

    # --- Cleanup ---
    os.remove(audio_path)
else:
    st.info("🎧 Please upload or record an audio clip to continue.")
