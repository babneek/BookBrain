import sys
import asyncio
from playwright_utils import scrape_wikisource_and_screenshot

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python wikisource_scraper.py <url> <text_output_path> <screenshot_output_path>")
        sys.exit(1)
    url, text_path, screenshot_path = sys.argv[1:]
    result = asyncio.run(scrape_wikisource_and_screenshot(url, text_path, screenshot_path))
    if result:
        print(f"Scraping and screenshot successful. Text saved to {text_path}, screenshot saved to {screenshot_path}.")
    else:
        print("Scraping and screenshot failed.") 