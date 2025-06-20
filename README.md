# BookBrain 📘

A modular, open-source app for uploading EPUB, PDF, or Wiki content, extracting chapters, generating AI-powered summaries, reviews, MCQs, and performing Q&A with feedback-driven retrieval.

---

## Features

- **Upload EPUB, PDF, or Wiki (Wikipedia/Wikisource) content**
- **Scrape chapters and take screenshots (Playwright)**
- **Generate summaries, reviews, and MCQs (Mistral LLM via Ollama)**
- **Interactive MCQ quiz with feedback and scoring**
- **Human-in-the-loop editing and regeneration of AI outputs**
- **Q&A with RL-inspired, feedback-weighted retrieval (ChromaDB)**
- **Versioning and consistent retrieval of all content**

---

## Setup

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd bookbrain
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

1. **Choose input type:** EPUB, PDF, or Wiki URL.
2. **Upload or enter URL.**
3. **Review, edit, and regenerate summaries, reviews, and MCQs.**
4. **Take MCQ quizzes and get instant feedback.**
5. **Ask questions and get answers influenced by user feedback.**
6. **Download your edited content.**

---

## Troubleshooting

- **Ollama not running:** Make sure the Ollama server is running and the Mistral model is pulled.
- **Playwright errors:** Run `playwright install` and ensure you have the required browsers.
- **ChromaDB issues:** The app stores embeddings in `./chroma_data` by default.

---

## License & Evaluation

This project is for evaluation/demo purposes only.  
All code is open-source and not intended for commercial use.

---

## Demo Video

- Show each feature: upload, scrape, AI generation, editing, MCQ quiz, Q&A, feedback, and RL search.
- Narrate how feedback influences future answers.

---

## Contact

For questions, contact [Your Name] or open an issue in the repo. 