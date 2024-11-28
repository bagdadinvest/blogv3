import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Runs the Django development server and starts BrowserSync for live reload'

    def handle(self, *args, **options):
        # Define the commands to run
        django_server_cmd = ["python", "manage.py", "runserver", "0.0.0.0:30000"]
        browser_sync_cmd = [
            "browser-sync",
            "start",
            "--proxy", "127.0.0.1:30000",  # Corrected the port
            "--files", "/home/lofa/Desktop/blogv3/**/*",  # Update this path as needed
            "--serveStatic", "/home/lofa/Desktop/blogv3/website/static/",  # Update this path as needed
            "--port", "3000",
        ]

        try:
            # Run Django server in a separate process
            print("Starting Django development server...")
            django_server = subprocess.Popen(django_server_cmd)

            # Run BrowserSync in a separate process
            print("Starting BrowserSync for live reloading...")
            browser_sync = subprocess.Popen(browser_sync_cmd)

            # Wait for both processes to complete
            django_server.wait()
            browser_sync.wait()

        except KeyboardInterrupt:
            # Handle manual interruption (Ctrl + C)
            print("\nStopping both processes...")
            try:
                django_server.terminate()
                browser_sync.terminate()
                django_server.wait()
                browser_sync.wait()
            except Exception as e:
                print(f"Error during termination: {e}")
            print("Processes terminated successfully.")

        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            # Ensure cleanup in case of errors
            try:
                if django_server.poll() is None:
                    django_server.terminate()
                if browser_sync.poll() is None:
                    browser_sync.terminate()
            except NameError:
                pass  # Processes were not started
            print("Cleanup complete.")
