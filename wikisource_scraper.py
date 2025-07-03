import sys
from wikisource_utils import scrape_wikisource

if __name__ == "__main__":
    print("[DEBUG] wikisource_scraper.py started.")
    print(f"[DEBUG] sys.argv: {sys.argv}")
    if len(sys.argv) != 3:
        print("Usage: python wikisource_scraper.py <url> <text_output_path>")
        sys.exit(1)
    url, text_path = sys.argv[1:]
    result = scrape_wikisource(url, text_path)
    if result:
        print(f"[RequestsBS4] Scraping successful. Text saved to {text_path}.")
    else:
        print("[RequestsBS4] Scraping failed.")
    print("[DEBUG] wikisource_scraper.py finished.") 