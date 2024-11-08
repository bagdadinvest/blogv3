# scraper/scraper.py

from playwright.sync_api import sync_playwright

def scrape_blog_content(url):
    """
    Scrapes blog content from the given URL.

    Parameters:
    - url (str): The URL to scrape.

    Returns:
    - dict: A dictionary containing the title, headers, and paragraphs.
    """
    scraped_data = {}

    with sync_playwright() as playwright:
        # Launch the browser in headless mode
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the provided URL
        print(f"Navigating to URL: {url}")
        page.goto(url)

        # Extracting the title of the page (h1)
        h1_elements = page.query_selector_all("h1")
        if h1_elements:
            scraped_data['title'] = h1_elements[0].inner_text()

        # Extracting headers (h2, h3, h4) and paragraphs
        headers = {
            'h2': [header.inner_text() for header in page.query_selector_all("h2")],
            'h3': [header.inner_text() for header in page.query_selector_all("h3")],
            'h4': [header.inner_text() for header in page.query_selector_all("h4")],
        }

        paragraphs = [p.inner_text() for p in page.query_selector_all("p")]

        scraped_data['headers'] = headers
        scraped_data['paragraphs'] = paragraphs

        # Close the browser
        browser.close()

    # Print scraped data for debugging purposes
    print(f"Scraped Data: {scraped_data}")
    return scraped_data
