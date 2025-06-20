import asyncio
from playwright.async_api import async_playwright, TimeoutError

async def scrape_wikisource_and_screenshot(url: str, text_path: str, screenshot_path: str, timeout: int = 15000) -> bool:
    """
    Scrape the main text from a Wikisource page and save a screenshot.
    Returns True if successful, False otherwise.
    """
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=timeout)
            text = await page.inner_text("body")
            await page.screenshot(path=screenshot_path, full_page=True)
            await browser.close()
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(text)
        return True
    except Exception as e:
        print(f"Playwright scrape error: {repr(e)}")
        return False

# Deprecated: Use scrape_wikisource_and_screenshot instead
async def scrape_wikisource(url: str, timeout: int = 15000) -> str:
    print("[DEPRECATED] Use scrape_wikisource_and_screenshot instead.")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=timeout)
            text = await page.inner_text("body")
            await browser.close()
        return text
    except Exception as e:
        print(f"Playwright error: {repr(e)}")
        return ""

async def scrape_and_screenshot(url: str, screenshot_path: str, timeout: int = 15000) -> None:
    print("[DEPRECATED] Use scrape_wikisource_and_screenshot instead.")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=timeout)
            await page.screenshot(path=screenshot_path, full_page=True)
            await browser.close()
    except Exception as e:
        print(f"Screenshot error: {repr(e)}") 