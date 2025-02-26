from PyQt5.QtCore import QObject, pyqtSignal
import requests
from m3u_filter.m3u_handler import download_m3u_xtream
import time

class DownloadWorker(QObject):
    progress = pyqtSignal(int)  # Progress percentage
    finished = pyqtSignal(str)  # Content
    error = pyqtSignal(str)     # Error message
    
    def __init__(self):
        super().__init__()
        self._cancelled = False
    
    def cancel(self):
        self._cancelled = True
    
    def download(self, source_type, params):
        try:
            if self._cancelled:
                return
                
            if source_type == "m3u_url":
                response = requests.get(params["url"], stream=True)
                response.raise_for_status()
                content_length = response.headers.get('content-length')
                
                if content_length:
                    content_length = int(content_length)
                    chunks = []
                    downloaded = 0
                    
                    for chunk in response.iter_content(chunk_size=8192):
                        if self._cancelled:
                            return
                        chunks.append(chunk)
                        downloaded += len(chunk)
                        progress = int((downloaded / content_length) * 100)
                        self.progress.emit(progress)
                        
                    content = b''.join(chunks).decode('utf-8')
                else:
                    content = response.text
                    
            elif source_type == "xtream":
                content = download_m3u_xtream(
                    params["base"],
                    params["username"],
                    params["password"]
                )
            else:  # file
                try:
                    # Try UTF-8 first
                    with open(params["file"], 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    # If UTF-8 fails, try with Latin-1
                    with open(params["file"], 'r', encoding='latin-1') as f:
                        content = f.read()
                    
            if not self._cancelled:
                self.finished.emit(content)
                
        except Exception as e:
            if not self._cancelled:
                self.error.emit(str(e))
