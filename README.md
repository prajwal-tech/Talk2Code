# Talk2Code (Offline)

## 🎤 Speak Your Idea → Get the Code
Talk2Code is an offline AI-powered tool that converts voice input into working code using open-source models. No APIs, no cloud processing—everything runs locally on your machine.

---

## 🚀 Features
- **Speech-to-Text:** Uses Whisper to transcribe spoken input into text.
- **Code Generation:** GPT4All generates code based on transcribed text.
- **Fully Offline:** No API calls, runs on your local device.
- **Real-Time Microphone Input:** Uses PyAudio or SoundDevice for live speech input.
- **Error Handling:** Ensures model files are correctly loaded before execution.
- **Save Generated Code:** Allows saving the generated code as a `.py` file.

---

## 🛠 Requirements
Install dependencies using the following command:
```bash
pip install streamlit torch whisper gpt4all sounddevice pyaudio
```

Make sure to download the **GPT4All model**:
1. Visit: [GPT4All Models](https://gpt4all.io/index.html)
2. Download `ggml-gpt4all-j-v1.3-groovy.bin`
3. Move it to the `models/` directory in your project folder.

---

## 🔧 How to Run
1. **Start the Streamlit App**
```bash
streamlit run app.py
```
2. **Use Your Microphone**
   - Speak your idea and let Whisper transcribe it.
   - The AI will generate the corresponding code.
3. **Save Your Code**
   - Click "Save Code" to download it as a `.py` file.

---

## 📂 Project Structure
```
📁 Talk2Code
│── 📁 models
│   └── ggml-gpt4all-j-v1.3-groovy.bin
│── app.py
│── requirements.txt
│── README.md
```

---

## 🤖 Future Improvements
- Add support for more programming languages.
- Implement real-time voice-to-code execution.
- Enhance accuracy with fine-tuned models.


