import streamlit as st
import tempfile
import os
from PyPDF2 import PdfReader
import wikipedia
import sys
import asyncio
from playwright_utils import scrape_wikisource_and_screenshot
from epub_utils import extract_chapters_from_epub
import subprocess
from chroma_utils import store_chapter_embeddings
import time
from sidebar_utils import show_sidebar

# --- WINDOWS EVENT LOOP FIX ---
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

st.set_page_config(page_title="BookBrain – Your AI Book Assistant", layout="wide", initial_sidebar_state="expanded", menu_items={"Get Help": None, "Report a bug": None, "About": None})
show_sidebar()

st.markdown("""
# 📘 BookBrain – Your AI Book Assistant
Welcome to BookBrain! Upload an EPUB, PDF, or enter a Wiki URL to extract chapters, generate AI-powered summaries, reviews, MCQs, and more.
---
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 📚 EPUB Upload")
    epub_file = st.file_uploader("Upload an EPUB file", type=["epub"], key="epub")
with col2:
    st.markdown("### 📄 PDF Upload")
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"], key="pdf")
with col3:
    st.markdown("### 🌐 Wiki URL")
    wiki_url = st.text_input("Enter a Wikipedia or Wikisource URL", key="wiki")
    wiki_btn = st.button("🔍 Process Wiki", key="wiki_btn")

# Extraction logic
if epub_file:
    with st.spinner("⏳ Processing EPUB..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp:
            tmp.write(epub_file.read())
            tmp_path = tmp.name
        chapter_titles, chapter_texts = extract_chapters_from_epub(tmp_path)
        # Split long chapters into sub-chapters
        max_len = 10000
        chunk_len = 8000
        new_titles = []
        new_texts = []
        for i, (title, text) in enumerate(zip(chapter_titles, chapter_texts)):
            if len(text) <= max_len:
                new_titles.append(title)
                new_texts.append(text)
            else:
                # Split into chunks
                num_chunks = (len(text) + chunk_len - 1) // chunk_len
                for j in range(num_chunks):
                    chunk_text = text[j*chunk_len:(j+1)*chunk_len]
                    if j == 0:
                        new_titles.append(title)
                    else:
                        new_titles.append(f"{title}.{j}")
                    new_texts.append(chunk_text)
        chapter_titles = new_titles
        chapter_texts = new_texts
        st.session_state["extracted_text"] = chapter_texts[0] if chapter_texts else ""
        st.session_state["source_type"] = "epub"
        st.session_state["chapters"] = chapter_texts
        st.session_state["chapter_titles"] = chapter_titles if chapter_titles else [f"Chapter {i}" for i in range(len(chapter_texts))]
        st.session_state["selected_chapter_idx"] = 0
        # Store in ChromaDB
        book_id = os.path.splitext(os.path.basename(epub_file.name))[0] if epub_file.name else f"epub_{int(time.time())}"
        store_chapter_embeddings(book_id, chapter_texts)
        st.session_state["book_id"] = book_id
        st.success("Chapters extracted and ready for AI processing!")

# Chapter selection dropdown (if chapters are present)
if "chapters" in st.session_state and st.session_state["chapters"]:
    st.markdown("---")
    prev_idx = st.session_state.get("selected_chapter_idx", 0)
    idx = st.selectbox(
        "Select Chapter:",
        options=list(range(len(st.session_state["chapters"]))),
        format_func=lambda i: st.session_state["chapter_titles"][i],
        index=prev_idx,
        key="chapter_select_box"
    )
    if idx != prev_idx:
        # Clear feature outputs when chapter changes
        for k in ["summary", "review", "mcqs", "last_answer", "last_question", "last_context_chunks"]:
            if k in st.session_state:
                del st.session_state[k]
    st.session_state["selected_chapter_idx"] = idx
    st.session_state["extracted_text"] = st.session_state["chapters"][idx]

elif pdf_file:
    with st.spinner("⏳ Processing PDF..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_file.read())
            tmp_path = tmp.name
        reader = PdfReader(tmp_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        st.session_state["extracted_text"] = text
        st.session_state["source_type"] = "pdf"
        # Split into ~1000 char chunks for embedding
        chunks = [text[i:i+1000] for i in range(0, len(text), 1000) if text[i:i+1000].strip()]
        book_id = os.path.splitext(os.path.basename(pdf_file.name))[0] if pdf_file.name else f"pdf_{int(time.time())}"
        store_chapter_embeddings(book_id, chunks)
        st.session_state["book_id"] = book_id
        st.success("PDF text extracted and ready for AI processing!")

elif wiki_url and wiki_btn:
    with st.spinner("⏳ Processing Wiki URL..."):
        text = ""
        if "wikisource.org" in wiki_url:
            text_path = "wikisource_text.txt"
            # No screenshot_path needed
            result = subprocess.run([
                sys.executable, "wikisource_scraper.py", wiki_url, text_path, "unused_screenshot.png"
            ], capture_output=True, text=True)
            # Always show scraper output for debugging
            st.write("Scraper stdout:", result.stdout)
            st.write("Scraper stderr:", result.stderr)
            st.write("Current directory:", os.getcwd())
            st.write("Files in directory:", os.listdir())
            if result.returncode != 0:
                st.error(f"Scraper error: {result.stderr}")
            # File existence check and debug output
            if not os.path.exists(text_path):
                st.error(f"File not found: {text_path}")
            else:
                with open(text_path, "r", encoding="utf-8") as f:
                    text = f.read()
                # Indicate which method was used
                if "[RequestsBS4] Scraping successful" in result.stdout:
                    st.info("Used requests+BeautifulSoup fallback for Wikisource scraping.")
                elif "Scraping and screenshot successful" in result.stdout:
                    st.success("Used Playwright for Wikisource scraping (screenshot available).")
                else:
                    st.warning("Wikisource scraping completed, but method could not be determined.")
        elif "wikipedia.org" in wiki_url:
            if "/wiki/" in wiki_url:
                title = wiki_url.split("/wiki/")[-1].replace("_", " ")
                text = wikipedia.page(title).content
            else:
                st.error("Invalid Wikipedia URL")
        else:
            st.error("Please enter a valid Wikipedia or Wikisource URL.")
        if text:
            st.session_state["extracted_text"] = text
            st.session_state["source_type"] = "wiki"
            # Split into ~1000 char chunks for embedding
            chunks = [text[i:i+1000] for i in range(0, len(text), 1000) if text[i:i+1000].strip()]
            book_id = wiki_url if wiki_url else f"wiki_{int(time.time())}"
            store_chapter_embeddings(book_id, chunks)
            st.session_state["book_id"] = book_id
            st.success("Wiki text extracted and ready for AI processing!")

# Show extracted content after processing
if "extracted_text" in st.session_state:
    st.markdown("---")
    st.markdown(
        """
        <div style='background-color: #f0f2f6; padding: 1.5em; border-radius: 10px; margin-bottom: 1em;'>
        <h3 style='margin-top:0;'>✅ Extracted Content</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f"<div style='background:#fff; border-radius:12px; padding:1.5em; margin-bottom:2em; max-height:400px; overflow:auto; font-size:1.1em; line-height:1.7;'>{st.session_state['extracted_text'][:5000].replace(chr(10),'<br>')}{'...' if len(st.session_state['extracted_text'])>5000 else ''}</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<center>Made with ❤️ by BookBrain</center>", unsafe_allow_html=True)
