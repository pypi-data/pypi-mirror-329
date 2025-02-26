import os
import hashlib
import logging
import requests
import threading
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

def fetch_icon(url, callback=None):
    """
    Fetch and return a QIcon for the given URL, caching it locally.
    If callback is provided, it will be called with the newly downloaded QIcon once ready.
    """
    if not url:
        return None

    cache_dir = os.path.join(os.path.dirname(__file__), "cache")
    os.makedirs(cache_dir, exist_ok=True)
    hash_name = hashlib.sha256(url.encode()).hexdigest() + ".png"
    file_path = os.path.join(cache_dir, hash_name)

    if os.path.exists(file_path):
        return QIcon(file_path)

    def download():
        try:
            r = requests.get(url, stream=True)
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            icon = QIcon(file_path)
            logging.info(f"Icon cached: {file_path}")
            if callback:
                QTimer.singleShot(0, lambda: callback(icon))
        except Exception as e:
            logging.error(f"Failed to download icon: {str(e)}")

    threading.Thread(target=download, daemon=True).start()
    return None
