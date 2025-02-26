import sys
import asyncio
import zendriver as zd
from readability import Document
from bs4 import BeautifulSoup

async def extract_content(url: str) -> str:
    # Start the browser in headless mode
    browser = await zd.start(headless=True)
    
    # Open the URL in a new tab and wait for it to load
    page = await browser.get(url)
    await page  # ensure page is loaded
    
    # Extract raw HTML content
    raw_html = await page.get_content()
    
    # Use readability-lxml to extract the main content HTML
    doc = Document(raw_html)
    main_html = doc.summary()
    
    # Use BeautifulSoup to remove any remaining HTML tags and get clean text
    soup = BeautifulSoup(main_html, "html.parser")
    main_text = soup.get_text(separator="\n", strip=True)
    
    await browser.stop()
    return main_text

def main():
    if len(sys.argv) != 2:
        print("Usage: atai-web-tool <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    try:
        main_text = asyncio.run(extract_content(url))
        print(main_text)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
