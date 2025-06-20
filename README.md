# BookBrain 📘

A modern, open-source app for uploading EPUB, PDF, or Wiki content, extracting chapters, and generating AI-powered summaries, reviews, MCQs, and Q&A with a beautiful, user-friendly interface.

---

## Features

- **Upload EPUB, PDF, or Wiki (Wikipedia/Wikisource) content**
- **Automatic chapter extraction** with dropdown chapter selection
- **Per-chapter features:**
  - Generate summaries, reviews, and MCQs for the selected chapter
  - Take MCQ quizzes with instant feedback, scoring, and motivational messages
  - Ask questions (Q/A) about the selected chapter with robust, context-aware answers
- **Persistent chapter list** until a new file is uploaded
- **Modern, colorful sidebar navigation** on every page
- **Elegant, responsive UI** with branding and clear layout
- **Robust Q/A pipeline** (no context length errors, always relevant answers)
- **Automatic MCQ retry** for reliable quiz generation
- **Download, regenerate, and edit all AI outputs**
- **Motivational feedback** after MCQ quizzes (e.g., "Excellent!", "Better luck next time!")

---

## Demo & Source

- **GitHub:** [https://github.com/babneek/BookBrain](https://github.com/babneek/BookBrain)
- **Author:** [babneek](https://github.com/babneek)

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/babneek/BookBrain.git
cd BookBrain
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Install and run Ollama (for Mistral LLM)
- [Ollama install instructions](https://ollama.com/download)
- Pull the Mistral model:
  ```bash
  ollama pull mistral
  ```
- Start the Ollama server (usually runs at `http://localhost:11434` by default).

### 4. Install Playwright browsers
```bash
playwright install
```

### 5. Run the app
```bash
streamlit run streamlit_app.py
```

---

## Usage

1. **Upload an EPUB, PDF, or enter a Wiki URL.**
2. **Select a chapter** from the dropdown (auto-detected, even for long books).
3. **Navigate using the sidebar** (Home, Summary, Review, MCQ, QA).
4. **Generate and edit summaries, reviews, and MCQs** for the selected chapter.
5. **Take MCQ quizzes** and get instant, colorful feedback and scoring.
6. **Ask questions (Q/A)** about the selected chapter and get detailed answers.
7. **Download or regenerate** any AI output.

---

## Screenshots

> Add your screenshots here for a visual overview!

---

## Troubleshooting

- **Ollama not running:** Make sure the Ollama server is running and the Mistral model is pulled.
- **Playwright errors:** Run `playwright install` and ensure you have the required browsers.
- **ChromaDB issues:** The app stores embeddings in `./chroma_data` by default.
- **Q/A or MCQ not working:** Make sure you have selected a chapter and uploaded valid content.

---

## License & Evaluation

This project is for evaluation/demo purposes only.

---

## Contributing

Pull requests and feedback are welcome! See [https://github.com/babneek/BookBrain](https://github.com/babneek/BookBrain) for issues and updates. 