import os
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from wagtail.images import get_image_model

def download_and_save_image(image_url):
    """
    Downloads an image from a URL and saves it to Wagtail's image model.
    """
    ImageModel = get_image_model()
    try:
        response = requests.get(image_url, stream=True, timeout=10)
        if response.status_code == 200:
            # Get the filename or use a default name
            filename = os.path.basename(image_url.split("?")[0]) or "downloaded_image.jpg"

            # Create a temporary file to hold the image data
            temp_file = NamedTemporaryFile(delete=False, suffix=".jpg")
            for chunk in response.iter_content(1024):
                temp_file.write(chunk)
            temp_file.seek(0)

            # Create a Wagtail image instance
            wagtail_image = ImageModel(title=filename)
            wagtail_image.file.save(filename, File(temp_file), save=True)
            print(f"Image downloaded and saved: {filename}")
            return wagtail_image
        else:
            print(f"Failed to download image: {image_url}, Status code: {response.status_code}")
            return None
    except requests.RequestException as req_ex:
        print(f"Image download failed for {image_url}: {req_ex}")
        return None
    except Exception as e:
        print(f"Unexpected error downloading {image_url}: {e}")
        return None

from django.shortcuts import render, redirect
from django.contrib import messages
from wagtail.models import Site
from .models import CustomArticlePage, ArticleIndexPage  # Import your model
from newspaper import Article

def article_from_url_view(request):
    """
    Admin view to scrape an article from a URL and save it as a CustomArticlePage.
    """
    print("View invoked.")

    if request.method == "POST":
        print("POST request received.")
        url = request.POST.get("article_url")
        print(f"URL received: {url}")

        if not url:
            messages.error(request, "Please provide a valid URL.")
            print("No URL provided.")
            return redirect("article_from_url")

        try:
            # Scrape the article using newspaper
            print("Initializing newspaper.Article...")
            article = Article(url)
            article.download()
            article.parse()
            print("Article downloaded and parsed.")

            # Extract data
            title = article.title or "Untitled Article"
            body = article.text or "No content available."
            top_image_url = article.top_image
            print(f"Scraped Title: {title}")
            print(f"Scraped Body Length: {len(body)} characters")
            print(f"Top Image URL: {top_image_url}")

            # Download the top image
            wagtail_image = None
            if top_image_url:
                wagtail_image = download_and_save_image(top_image_url)
                if wagtail_image:
                    print(f"Top image saved with title: {wagtail_image.title}")

            # Find parent page
            parent_page = ArticleIndexPage.objects.live().first()
            if not parent_page:
                messages.error(request, "No parent ArticleIndexPage found.")
                print("No parent ArticleIndexPage found.")
                return redirect("article_from_url")
            print(f"Parent Page Found: {parent_page}")

            # Create and save the page
            print("Creating CustomArticlePage instance...")
            article_page = CustomArticlePage(
                title=title,
                body=[{"type": "rich_text", "value": body}],  # Valid StreamField content
                caption="Default caption",  # Provide default value
                author_display="Unknown Author",  # Provide default value
                content_body=body,  # Populate optional content_body field
                live=True,  # Set live by default
            )
            # Associate the downloaded image with the page if available
            if wagtail_image:
                article_page.hero_image = wagtail_image  # Assuming a hero_image ForeignKey field

            parent_page.add_child(instance=article_page)
            print("CustomArticlePage instance added as a child.")
            article_page.save()
            print("CustomArticlePage instance saved successfully.")

            messages.success(request, f"Article '{title}' saved successfully!")
            return redirect("wagtailadmin_explore_root")
        except Exception as e:
            print(f"Error occurred: {e}")
            messages.error(request, f"Failed to save article: {e}")
            return redirect("article_from_url")

    # Render the input form
    print("Rendering input form...")
    return render(request, "admin/article_from_url.html")
