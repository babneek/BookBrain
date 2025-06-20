from ebooklib import epub
from bs4 import BeautifulSoup

def extract_chapters_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    toc = book.toc
    items = {item.get_name(): item for item in book.get_items() if item.get_type() == 9}
    chapter_texts = []

    def process_entry(entry):
        if isinstance(entry, tuple):
            link = entry[0]
            subs = entry[1]
        else:
            link = entry
            subs = []
        href = getattr(link, 'href', None)
        if href and href in items:
            item = items[href]
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            if len(text) > 50:
                chapter_texts.append(text)
        for sub in subs:
            process_entry(sub)

    for entry in toc:
        process_entry(entry)

    if not chapter_texts:
        for item in book.get_items():
            if item.get_type() == 9:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text = soup.get_text(separator=' ', strip=True)
                if len(text) > 50:
                    chapter_texts.append(text)

    if not chapter_texts:
        chapter_texts = ["(No chapters found or could not extract text)"]

    # Format chapter titles as 'Chapter 0', 'Chapter 1', ...
    chapter_titles = [f"Chapter {i}" for i in range(len(chapter_texts))]

    return chapter_titles, chapter_texts 