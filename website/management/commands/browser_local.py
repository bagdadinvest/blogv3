import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Runs the Django development server and starts browser-sync for live reload'

    def handle(self, *args, **options):
        # Define the commands to run
        django_server_cmd = ["python", "manage.py", "runserver", "0.0.0.0:30000"]
        browser_sync_cmd = [
            "browser-sync",
            "start",
            "--proxy", "127.0.0.1:300000",
            "--files", "/home/lotfikan/blogv3/**/*",  # Update the path here
            "--serveStatic", "/home/lotfikan/blogv3/website/static/",  # Update the path here
            "--port", "3000",
        ]

        try:
            # Run Django server in a separate process
            print("Starting Django development server...")
            django_server = subprocess.Popen(django_server_cmd)

            # Run browser-sync in a separate process
            print("Starting Browser Sync for live reloading...")
            browser_sync = subprocess.Popen(browser_sync_cmd)

            # Wait for both processes to complete
            django_server.wait()
            browser_sync.wait()

        except KeyboardInterrupt:
            # Handle manual interruption (Ctrl + C)
            print("Stopping both processes...")
            django_server.terminate()
            browser_sync.terminate()
            print("Processes terminated successfully.")
        except Exception as e:
            print(f"Error occurred: {e}")
