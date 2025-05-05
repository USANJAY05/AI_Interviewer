
# 🧠 AI Interviewer

An interactive AI-powered voice-based interviewer that listens, responds, and evaluates your answers — just like a real human! This project uses **LangChain**, **speech recognition**, **pyttsx3**, and **Ollama** to run LLMs locally.

## 🚀 Features

- 🎤 Convert speech to text using `speech_recognition`
- 🗣️ Responds using offline text-to-speech (`pyttsx3`)
- 🤖 AI-generated dynamic questions with **LangChain**
- 🧠 Local LLM integration via **Ollama**
- 🔁 Voice-driven interactive interview loop

## 🛠️ Tech Stack

- **Python 3.10+**
- **LangChain**
- **Ollama** (locally running LLM like `llama3`, `mistral`, etc.)
- **pyttsx3** – Text-to-Speech
- **speech_recognition** – Speech-to-Text

## 📦 Installation

1. **Clone the repo**

```bash
git clone https://github.com/USANJAY05/ai-interviewer.git
cd ai-interviewer
````

2. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

3. **Install and run Ollama**

Install Ollama from: [https://ollama.com/download](https://ollama.com/download)

Then pull your preferred model:

```bash
ollama pull llama3
```

Or use another like:

```bash
ollama pull mistral
```

4. **Configure environment**

```env
LANGCHAIN_TRACING_V2=false
```

(You may not need an API key since you're using Ollama locally.)

## 🧪 How to Run

```bash
python app.py
```

🗣️ The AI will ask questions aloud. You answer using your mic. It listens, processes, and continues the conversation intelligently.

## 📸 Preview

*(Add screenshots or CLI output if available)*

## 💡 Future Enhancements

* 📊 Add scoring/evaluation metrics
* 📝 Export Q\&A transcript
* 🖼️ Build a simple frontend interface

## 🏷️ Models You Can Use

* `llama3`
* `mistral`
* `gemma`
* Any compatible Ollama-supported LLM

> 🔧 Update the LangChain `llm` config to match the pulled model.

## 📬 Contact

**Sanjay U**
📧 [sanjay.05@icloud.com](mailto:sanjay.05@icloud.com)
🌐 [Portfolio](https://sanjaypotfolio.netlify.app)
🔗 [LinkedIn](https://www.linkedin.com/in/sanjay-u-551b21255/)

---
