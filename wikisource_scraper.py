import sys
import asyncio
from playwright_utils import scrape_wikisource_and_screenshot, scrape_wikisource_requests_bs4

if __name__ == "__main__":
    print("[DEBUG] wikisource_scraper.py started.")
    print(f"[DEBUG] sys.argv: {sys.argv}")
    if len(sys.argv) != 4:
        print("Usage: python wikisource_scraper.py <url> <text_output_path> <screenshot_output_path>")
        sys.exit(1)
    url, text_path, screenshot_path = sys.argv[1:]
    # Try Playwright first, then fallback to requests+bs4
    try:
        print("[DEBUG] Trying Playwright-based scraper...")
        result = asyncio.run(scrape_wikisource_and_screenshot(url, text_path, screenshot_path))
        if result:
            print(f"Scraping and screenshot successful. Text saved to {text_path}, screenshot saved to {screenshot_path}.")
        else:
            print("[DEBUG] Playwright failed, trying requests+BeautifulSoup fallback...")
            result2 = scrape_wikisource_requests_bs4(url, text_path)
            if result2:
                print(f"[RequestsBS4] Scraping successful. Text saved to {text_path}.")
            else:
                print("[RequestsBS4] Scraping failed.")
    except Exception as e:
        print(f"[ERROR] Exception in wikisource_scraper.py: {e}")
        import traceback
        traceback.print_exc()
        print("[DEBUG] Trying requests+BeautifulSoup fallback after exception...")
        result2 = scrape_wikisource_requests_bs4(url, text_path)
        if result2:
            print(f"[RequestsBS4] Scraping successful. Text saved to {text_path}.")
        else:
            print("[RequestsBS4] Scraping failed.")
        sys.exit(2)
    print("[DEBUG] wikisource_scraper.py finished.") 