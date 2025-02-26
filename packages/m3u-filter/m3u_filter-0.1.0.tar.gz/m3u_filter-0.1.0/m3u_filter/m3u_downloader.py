from PyQt5.QtCore import QObject, QThread
from PyQt5.QtWidgets import QPushButton, QMessageBox
from m3u_filter.progress_widget import ProgressWidget
from m3u_filter.download_worker import DownloadWorker
import os
import urllib.parse
import requests
from m3u_filter.m3u_handler import download_m3u_xtream

class M3UDownloader(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.download_thread = None
        self.download_worker = None
        self.current_categories = {"livetv"}  # Default to Live TV
        
    def start_download(self, source_type, params, categories, progress_widget, on_complete):
        """Start download with progress tracking and filtering."""
        self.progress = progress_widget
        self.on_complete = on_complete
        self.current_categories = categories  # Store categories for this download
        self.progress.start_progress("Downloading...")
        
        # Create worker and thread
        self.download_thread = QThread()
        self.download_worker = DownloadWorker()
        self.download_worker.moveToThread(self.download_thread)
        
        # Connect signals
        self.download_worker.progress.connect(self.progress.update_progress)
        self.download_worker.finished.connect(
            lambda content: self._on_download_complete(content, source_type, params)
        )
        self.download_worker.error.connect(self._on_download_error)
        
        # Start download with category filtering
        self.download_thread.started.connect(
            lambda: self.download_worker.download(source_type, params)
        )
        
        # Add cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.cancel)
        self.progress.layout().addWidget(cancel_btn)
        
        self.download_thread.start()

    def cancel(self):
        if self.download_worker:
            self.download_worker.cancel()
            self.progress.finish("Cancelled", 2000)
            self.download_thread.quit()
            self.download_thread.wait()

    def _on_download_complete(self, content, source_type, params):
        """Filter content after download completes."""
        self.download_thread.quit()
        self.download_thread.wait()
        try:
            filtered_lines = ['#EXTM3U']
            lines = content.splitlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith("#EXTINF:"):
                    next_url = lines[i + 1].strip() if i + 1 < len(lines) else ""
                    path = urllib.parse.urlparse(next_url).path.lower()
                    
                    # Simple path-based category detection
                    if path.startswith("/movie"):
                        cat = "movie"
                    elif path.startswith("/series"):
                        cat = "series"
                    else:
                        cat = "livetv"

                    if cat in self.current_categories:
                        filtered_lines.append(line)
                        filtered_lines.append(next_url)
                    i += 2
                else:
                    if not line.startswith("#EXTM3U"):
                        filtered_lines.append(line)
                    i += 1

            final_content = "\n".join(filtered_lines)
            self.progress.finish("Done", 2000)
            self.on_complete(final_content)
        except Exception as e:
            self._on_download_error(str(e))

    def _on_download_error(self, error):
        self.download_thread.quit()
        self.download_thread.wait()
        self.progress.finish(f"Error: {error}", 2000)
        QMessageBox.critical(self.parent, "Download Error", str(error))
