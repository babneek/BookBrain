# BookBrain 📘

BookBrain is a modern, open-source app for reading, exploring, and learning from books and documents using AI. Upload EPUB, PDF, or Wiki content, extract chapters, and generate AI-powered summaries, reviews, MCQs, and Q&A—all with a beautiful, user-friendly interface.

---

## Features

- **Upload EPUB, PDF, or Wiki (Wikipedia/Wikisource) content**
- **Automatic chapter extraction** with a dropdown for easy chapter selection
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

## How It Works

1. **Upload Content:**
   - Upload an EPUB, PDF, or enter a Wiki URL.
   - The app extracts chapters automatically and displays them in a dropdown.
2. **Select a Chapter:**
   - Choose any chapter to work with. The chapter list stays until you upload new content.
3. **Explore Features:**
   - **Summary:** Get a detailed, multi-paragraph summary of the selected chapter.
   - **Review:** Generate a comprehensive review, including themes and analysis.
   - **MCQ Quiz:** Instantly generate and take a quiz for the chapter, with feedback and scoring.
   - **Q/A:** Ask any question about the selected chapter and get a detailed, context-aware answer.
4. **Edit, Regenerate, Download:**
   - All AI outputs can be edited, regenerated, or downloaded for your notes.
5. **Navigation:**
   - Use the sidebar to switch between features. The UI is modern, colorful, and easy to use.

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

### 3. Install Playwright browsers (for Wiki scraping)
```bash
playwright install
```

### 4. Configure your LLM API
- BookBrain uses OpenRouter, OpenAI, or your preferred LLM API for all AI features.
- Set your API key in a `.env` file or as an environment variable (see `.env.example` if provided).

### 5. Run the app
```bash
streamlit run streamlit_app.py
```

---

## 🚀 Deployment

### AWS App Runner (Recommended)

AWS App Runner provides excellent Python support and is perfect for BookBrain:

1. **Sign up** for an AWS account at [aws.amazon.com](https://aws.amazon.com)
2. **Go to AWS App Runner** console and click "Create service"
3. **Connect your GitHub** account and select your BookBrain repository
4. **Configure the service:**
   - Runtime: Docker
   - Port: 8080
   - CPU: 1 vCPU, Memory: 2 GB
5. **Set environment variables:**
   - `OPENAI_API_KEY`: Your OpenRouter or OpenAI API key
   - `OPENROUTER_MODEL`: (Optional) Specify a different model
6. **Deploy!** Your app will be live in 5-10 minutes

**Live Demo:** [BookBrain on AWS](https://bookbrain-app.awsapprunner.com) *(Coming soon)*

📖 **Detailed AWS Deployment Guide:** See [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md)

### Alternative Deployment Options

- **Railway:** Use the provided `railway.json` configuration
- **Render:** Use the provided `requirements.txt` and `Procfile`
- **Heroku:** Use the provided `requirements.txt` and `Procfile`
- **Streamlit Cloud:** May have compatibility issues with ChromaDB
- **Local:** Follow the setup instructions above

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

## Troubleshooting

- **API errors:** Make sure your LLM API key is set and valid.
- **Playwright errors:** Run `playwright install` and ensure you have the required browsers.
- **ChromaDB issues:** The app stores embeddings in `./chroma_data` by default.
- **Q/A or MCQ not working:** Make sure you have selected a chapter and uploaded valid content.

---

## Screenshots

> Add your screenshots here for a visual overview!

---

## License & Contributing

This project is for evaluation/demo purposes only. Pull requests and feedback are welcome!

- **GitHub:** [https://github.com/babneek/BookBrain](https://github.com/babneek/BookBrain)
- **Author:** [babneek](https://github.com/babneek) 