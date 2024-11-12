# website/utils.py

from website.models import CustomArticlePage
from wagtail.models import Page
from scraper.scraper import scrape_blog_content

def create_custom_article_page(parent_page, url):
    """
    Creates a CustomArticlePage instance with scraped content.

    Parameters:
    - parent_page (Page): The parent page under which the article will be created.
    - url (str): The URL to scrape content from.

    Returns:
    - CustomArticlePage: The created page instance.
    """
    scraped_data = scrape_blog_content(url)

    # Create the page
    new_article_page = CustomArticlePage(
        title=scraped_data['title'],
        content_body=scraped_data['html_content']
    )

    # Add the new page under the parent page
    parent_page.add_child(instance=new_article_page)
    new_article_page.save_revision().publish()

    return new_article_page
