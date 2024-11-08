import os
import django
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the settings module to your project settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings.dev')

# Setup Django to ensure everything initializes properly
django.setup()

# Import necessary modules for Wagtail and your custom article model
from wagtail.fields import StreamValue
from website.models import ArticleIndexPage, CustomArticlePage  # Import CustomArticlePage
from django.utils.text import slugify
from django.utils import timezone
from scraper.scraper import scrape_blog_content
from coderedcms.blocks import CONTENT_STREAMBLOCKS

def map_scraped_data_to_custom_article(scraped_data):
    """
    Maps the scraped data to a Custom Article Page model.

    Parameters:
    - scraped_data (dict): The data returned from the scraping function
    """

    # Step 1: Find the existing ArticleIndexPage to use as the parent for new articles
    parent_page = ArticleIndexPage.objects.live().first()

    if not parent_page:
        print("Error: No ArticleIndexPage found to add the article to. Please create one in the Wagtail admin.")
        return

    # Step 2: Creating a unique slug for the article
    title = scraped_data.get('title', 'Untitled')
    slug = slugify(title)

    # Check if an article with the same slug already exists
    if CustomArticlePage.objects.filter(slug=slug).exists():
        print(f"Article with slug '{slug}' already exists. Skipping creation.")
        return

    # Step 3: Create StreamField content for the body using CONTENT_STREAMBLOCKS
    stream_data = []

    # Adding headers (h2, h3, h4) to the StreamField
    for level, headers in scraped_data.get('headers', {}).items():
        for header_text in headers:
            if header_text:  # Ensuring the text is not empty
                stream_data.append({
                    'type': 'heading',  # Assuming CONTENT_STREAMBLOCKS has a "heading" block
                    'value': {
                        'heading_text': header_text,
                        'size': level  # Assuming 'size' is correctly set up in CONTENT_STREAMBLOCKS as an option
                    }
                })

    # Adding paragraphs to the StreamField
    for paragraph in scraped_data.get('paragraphs', []):
        if paragraph:  # Ensuring the text is not empty
            stream_data.append({
                'type': 'richtext',  # Assuming CONTENT_STREAMBLOCKS has a "richtext" block
                'value': paragraph,
            })

    # Convert stream_data into StreamField value
    try:
        # Use CONTENT_STREAMBLOCKS directly to create StreamValue
        stream_field = StreamValue(
            CONTENT_STREAMBLOCKS,
            stream_data,
            is_lazy=True
        )
    except Exception as e:
        print(f"Error creating StreamValue: {e}")
        return

    # Step 4: Create a new CustomArticlePage instance using custom_body
    new_article = CustomArticlePage(
        title=title,
        slug=slug,
        custom_body=stream_field,  # Use custom_body instead of body
        first_published_at=timezone.now(),  # Optionally set publish date
    )

    # Step 5: Add the article as a child of the parent page
    parent_page.add_child(instance=new_article)

    # Step 6: Publish the new article page
    new_article.save_revision().publish()

    print(f"Successfully created and published article: {title}")

# Example usage with an actual URL
url_to_scrape = "https://dentakay.com/implants-vs-dentures-functions-structure-and-costs/"
scraped_content = scrape_blog_content(url_to_scrape)

# Map the scraped content to an article page in Wagtail
if scraped_content:
    map_scraped_data_to_custom_article(scraped_content)
