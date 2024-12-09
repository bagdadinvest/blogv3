# views.py

import os
import tempfile
import subprocess
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.images.models import Image
from wagtail.documents.models import Document
from wagtailmedia.models import Media
from django.conf import settings

def article_from_url_view(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            messages.error(request, "Please provide a URL.")
            return redirect(reverse('article_from_url'))

        try:
            # Create a temporary directory to store the downloaded media
            with tempfile.TemporaryDirectory() as tmpdirname:
                # Use you-get to download the media
                # You can use you-get as a subprocess or as a library
                # Here, we'll use subprocess for simplicity
                subprocess.run(['you-get', '-o', tmpdirname, url], check=True)

                # Find the downloaded file
                downloaded_files = os.listdir(tmpdirname)
                if not downloaded_files:
                    messages.error(request, "No media was downloaded from the provided URL.")
                    return redirect(reverse('article_from_url'))

                downloaded_file_path = os.path.join(tmpdirname, downloaded_files[0])

                # Determine the type of media
                file_extension = os.path.splitext(downloaded_file_path)[1].lower()
                if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                    # It's an image
                    with open(downloaded_file_path, 'rb') as f:
                        image = Image.objects.create(
                            title=downloaded_files[0],
                            file=f
                        )
                    messages.success(request, f"Image '{image.title}' uploaded successfully.")
                elif file_extension in ['.mp4', '.avi', '.mov', '.wmv', '.flv']:
                    # It's a video; use Media model
                    with open(downloaded_file_path, 'rb') as f:
                        media = Media.objects.create(
                            title=downloaded_files[0],
                            file=f
                        )
                    messages.success(request, f"Media '{media.title}' uploaded successfully.")
                elif file_extension in ['.pdf', '.docx', '.xlsx', '.pptx']:
                    # It's a document
                    with open(downloaded_file_path, 'rb') as f:
                        document = Document.objects.create(
                            title=downloaded_files[0],
                            file=f
                        )
                    messages.success(request, f"Document '{document.title}' uploaded successfully.")
                else:
                    messages.warning(request, f"Downloaded file '{downloaded_files[0]}' has an unsupported file type.")
        except subprocess.CalledProcessError as e:
            messages.error(request, f"Error downloading media: {str(e)}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

        return redirect(reverse('article_from_url'))

    return render(request, 'admin/article_from_url.html')
