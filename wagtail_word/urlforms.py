import requests
from bs4 import BeautifulSoup
from django import forms
from wagtail.admin.forms import WagtailAdminPageForm
import logging

# Set up basic logging to console for debug statements
logging.basicConfig(level=logging.DEBUG)

class BlogURLForm(WagtailAdminPageForm):
    url = forms.URLField(
        label='Blog URL',
        help_text='Enter the URL of the blog',
        required=True,
    )

    def clean_url(self):
        url = self.cleaned_data['url']
        logging.debug(f"Received URL: {url}")

        # Validate if the URL is reachable
        try:
            response = requests.get(url)
            if response.status_code != 200:
                logging.error(f"Failed to retrieve content. Status Code: {response.status_code}")
                raise forms.ValidationError("Could not retrieve the blog content.")
        except requests.RequestException as e:
            logging.exception(f"Error in URL request: {e}")
            raise forms.ValidationError("Invalid URL or failed to retrieve content.")

        logging.debug("URL successfully validated.")
        return url

    def fetch_blog_content(self, url):
        """Fetch the blog content from the provided URL."""
        logging.debug(f"Attempting to fetch content from: {url}")

        try:
            response = requests.get(url)
            response.raise_for_status()  # Ensure we got a valid response
            logging.debug(f"Content fetched successfully from: {url}")
            return response.content
        except requests.RequestException as e:
            logging.exception(f"Error fetching content from URL: {e}")
            raise forms.ValidationError(f"Error fetching content from URL: {e}")

    def parse_html_content(self, html_content):
        """Parse HTML content to extract the blog title, paragraphs, images, links, etc."""
        logging.debug("Parsing HTML content.")

        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the blog title
        title = soup.find('title').get_text(strip=True)
        logging.debug(f"Extracted title: {title}")

        # Extract paragraphs
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
        logging.debug(f"Extracted {len(paragraphs)} paragraphs.")

        # Extract images
        images = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]
        logging.debug(f"Extracted {len(images)} images.")

        # Extract hyperlinks
        links = {a.get_text(strip=True): a['href'] for a in soup.find_all('a') if 'href' in a.attrs}
        logging.debug(f"Extracted {len(links)} hyperlinks.")

        # Returning parsed content
        return {
            'title': title,
            'content': '\n'.join(paragraphs),
            'images': images,
            'links': links
        }

    def convert_to_richtext(self, parsed_content):
        """Convert parsed blog content to Wagtail-compatible rich text format (HTML)."""
        logging.debug("Converting parsed content to Wagtail-compatible RichTextField format.")

        # Convert title to h1
        rich_text_content = f"<h1>{parsed_content['title']}</h1>"

        # Convert paragraphs to <p> tags
        rich_text_content += ''.join([f"<p>{para}</p>" for para in parsed_content['content'].split('\n')])

        # Convert images to embed format
        for img_src in parsed_content['images']:
            rich_text_content += f'<img src="{img_src}" alt="Image"/>'

        # Convert hyperlinks to <a> tags
        for link_text, href in parsed_content['links'].items():
            rich_text_content += f'<a href="{href}">{link_text}</a>'

        logging.debug("Content conversion to RichTextField complete.")
        return rich_text_content

    def save(self, commit=True):
        """Override the save method to process the URL and convert its content."""
        logging.debug("Initiating save process.")

        instance = super().save(commit=False)
        url = self.cleaned_data['url']

        # Fetch and parse the blog content
        try:
            html_content = self.fetch_blog_content(url)
            parsed_content = self.parse_html_content(html_content)

            # Convert to Wagtail-compatible rich text
            richtext_content = self.convert_to_richtext(parsed_content)

            # Assuming your Wagtail page model has a RichTextField for blog content
            instance.set_content(richtext_content)  # Align with the forms.py structure

            logging.debug("Content saved successfully.")
        except Exception as e:
            logging.exception(f"An error occurred while processing the URL content: {e}")
            raise forms.ValidationError(f"An error occurred: {e}")

        if commit:
            instance.save()
            logging.debug("Instance saved to the database.")

        return instance
