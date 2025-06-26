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

### 4. (Optional, for local Wikisource screenshots) Install Playwright browsers
If you want to use Playwright for Wikisource scraping (with screenshots) **locally**, run:
```bash
playwright install
```

> **Note:** On Streamlit Cloud, Playwright is not used for Wikisource scraping due to browser sandboxing and installation limitations. Instead, the app uses a robust fallback with `requests` and `BeautifulSoup` for text extraction only (no screenshots). This ensures compatibility and reliability in the cloud environment.

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
- **Playwright errors (local only):** Run `playwright install` to install required browsers. On Streamlit Cloud, Playwright is not used.
- **ChromaDB issues:** The app stores embeddings in `./chroma_data` by default. Make sure you have write permissions.
- **Q/A or MCQ not working:** Ensure you have selected a chapter and uploaded valid content.
- **Import errors:** Make sure you're running the app from the project root directory.

### Getting Help

If you encounter any issues:
1. Check that all dependencies are installed correctly
2. Verify your API key is set and working
3. Ensure you're using Python 3.10 or higher
4. Try running `streamlit run streamlit_app.py --logger.level debug` for detailed logs

---

## Features in Detail

### Semantic Search
- Uses ChromaDB for storing and retrieving document embeddings
- Enables advanced content search across your uploaded books
- Automatically indexes chapters for quick retrieval

### Content Versioning
- Tracks different versions of summaries, reviews, and MCQs
- Allows you to compare and revert to previous versions
- Maintains history of your AI-generated content

### Robust Error Handling
- Graceful fallbacks when APIs are unavailable
- Automatic retry mechanisms for failed requests
- User-friendly error messages

---

## Contributing

This project is open for contributions! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation

---

## License

This project is for evaluation and educational purposes. Feel free to use and modify for your own projects.

---

## Screenshots

> Add your screenshots here for a visual overview!

---

**GitHub:** [https://github.com/babneek/BookBrain](https://github.com/babneek/BookBrain)  
**Author:** [babneek](https://github.com/babneek) 