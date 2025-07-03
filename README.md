# BookBrain 📘

BookBrain is a modern, open-source app for reading, exploring, and learning from books and documents using AI. Upload EPUB, PDF, or Wiki content, extract chapters, and generate AI-powered summaries, reviews, MCQs, and Q&A—all with a beautiful, user-friendly interface.

---

## 🚀 Live Demo
Try BookBrain instantly on Streamlit Cloud:
[https://bookbrain-u3fr2gvvdxeesm3bfsl4on.streamlit.app/Summary](https://bookbrain-u3fr2gvvdxeesm3bfsl4on.streamlit.app/Summary)

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
- **Semantic search** with ChromaDB for advanced content exploration
- **Content versioning** to track changes and improvements
- **Clean, user-friendly UI with robust error handling**

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

## Local Setup

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone the repository
```bash
git clone https://github.com/babneek/BookBrain.git
cd BookBrain
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. (No Playwright needed) Wikisource scraping uses requests+BeautifulSoup
Wikisource scraping is now handled using requests and BeautifulSoup only. No browser or Playwright setup is required.

> **Note:** Screenshots of Wikisource pages are no longer supported. The app uses a robust fallback with `requests` and `BeautifulSoup` for text extraction only. This ensures compatibility and reliability in all environments.

### 5. Configure your LLM API
Create a `.env` file in the project root with your API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

**Supported APIs:**
- OpenAI API
- OpenRouter API
- Any other compatible LLM API

### 6. Run the app
```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

---

## How to Deploy on Streamlit Cloud

1. Push your code to a public GitHub repository.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in with GitHub.
3. Click "New app", select your repo and branch, and set the main file to `streamlit_app.py`.
4. **No Playwright setup is needed for cloud deployment.** The app will automatically use the requests+BeautifulSoup fallback for Wikisource scraping.
5. Click "Deploy" and enjoy your app online!

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

## Project Structure

```
bookbrain/
├── chroma_utils.py           # ChromaDB and semantic search utilities
├── epub_utils.py             # EPUB processing utilities
├── LICENSE                   # License file
├── llm_utils.py              # LLM API integration
├── pages/                    # Streamlit pages
│   ├── 1_Summary.py          # Summary generation page
│   ├── 2_Review.py           # Review generation page
│   ├── 3_MCQ.py              # MCQ quiz page
│   └── 4_QA.py               # Q&A page
├── pipeline.py               # Core processing pipeline
├── playwright_utils.py       # Web scraping utilities (Playwright for local, requests+bs4 for cloud)
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── sidebar_utils.py          # Sidebar navigation
├── streamlit_app.py          # Main Streamlit application
├── wikisource_scraper.py     # Wiki scraping utilities
```

---

## Troubleshooting

### Common Issues

- **API errors:** Make sure your LLM API key is set in the `.env` file and is valid.
- **Playwright errors:** Playwright is no longer required. All scraping is handled with requests+BeautifulSoup.
- **ChromaDB issues:** The app stores embeddings in `