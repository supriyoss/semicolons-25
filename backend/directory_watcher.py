import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from pdf_processor import process_pdf_file


class UploadEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Check if it's a file (not a directory)
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            process_new_file(event.src_path)


def process_new_file(file_path):
    """Process the new file - Placeholder function"""
    if file_path.lower().endswith(".pdf"):
        process_pdf_file(file_path)
    else:
        print("Unsupported file type. Only PDFs are processed.")


def start_monitoring(folder_path):
    event_handler = UploadEventHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    print(f"Monitoring '{folder_path}' for new files...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    uploads_folder = "uploads"
    os.makedirs(uploads_folder, exist_ok=True)  # Ensure the folder exists
    start_monitoring(uploads_folder)

"""
Running the Script as a Background Service

Linux: Run as a Systemd Service

1. Create a systemd service file:

sudo nano /etc/systemd/system/directory_watcher.service
2. Add the following content(replace paths accordingly):

[Unit]
Description = Python Directory Watcher
After = network.target

[Service]
ExecStart = /usr/bin/python3/path/to/directory_watcher.py
Restart = always
User = your-username
WorkingDirectory =/path/to/
StandardOutput = append:/path/to/directory_watcher.log
StandardError = append:/path/to/directory_watcher.log

[Install]
WantedBy = multi - user.target



3. Enable and start the service:

sudo systemctl daemon-reload
sudo systemctl enable directory_watcher
sudo systemctl start directory_watcher
sudo systemctl status directory_watcher
"""
