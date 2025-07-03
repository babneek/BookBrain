def scrape_wikisource(url: str, text_path: str) -> bool:
    """
    Scrape the main text from a Wikisource page using requests and BeautifulSoup.
    Saves the text to text_path. Returns True if successful, False otherwise.
    """
    try:
        import requests
        from bs4 import BeautifulSoup, Tag
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        main = soup.find('div', id='ws-content') or soup.find('div', class_='mw-parser-output')
        if not main or not isinstance(main, Tag):
            print("[RequestsBS4] Could not find main content div or it is not a Tag.")
            return False
        text = '\n'.join(p.get_text(separator=' ', strip=True) for p in main.find_all(['p', 'div', 'span', 'li']))
        if not text.strip():
            print("[RequestsBS4] No text extracted from main content.")
            return False
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"[RequestsBS4] Error: {e}")
        return False 