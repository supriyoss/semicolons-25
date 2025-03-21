"""Python Code: Directory Listener
This script continuously listens for newly created files (e.g., PDFs) and processes them.

Install Dependencies
pip install watchdog
Save this as directory_watcher.py:
"""
import time
import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(
    filename="directory_watcher.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

WATCH_DIRECTORY = "/path/to/watch"  # Change this to the folder you want to monitor


class PDFHandler(FileSystemEventHandler):
    """Handles newly created PDF files in the directory"""

    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith('.pdf'):
            logging.info(f"New PDF detected: {event.src_path}")
            self.process_pdf(event.src_path)

    def process_pdf(self, pdf_path):
        """Process the PDF file (modify this function as needed)"""
        logging.info(f"Processing PDF: {pdf_path}")
        # Add your PDF processing code here


def start_watching():
    """Starts watching the directory for changes"""
    observer = Observer()
    event_handler = PDFHandler()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=False)

    observer.start()
    logging.info("Started watching directory: " + WATCH_DIRECTORY)

    try:
        while True:
            time.sleep(1)  # Keep running
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Stopped watching directory")
    observer.join()


if __name__ == "__main__":
    start_watching()
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