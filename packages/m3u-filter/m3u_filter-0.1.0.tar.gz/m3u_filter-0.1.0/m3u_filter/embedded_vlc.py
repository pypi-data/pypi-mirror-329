import logging
try:
    import vlc
except ImportError:
    vlc = None

import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from m3u_filter.vlc_manager import VLCManager

class EmbeddedVLC(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        if vlc is None:
            logging.warning("python-vlc is not installed.")
            QMessageBox.information(
                self,
                "VLC Not Installed",
                "python-vlc could not be imported. Please install with: pip install python-vlc"
            )
            self.setDisabled(True)
            return
        
        logging.info("EmbeddedVLC: python-vlc imported successfully.")
        self.instance = vlc.Instance("--no-xlib")
        self.player = self.instance.media_player_new()
        self.video_frame = QWidget(self)
        self.video_frame.setStyleSheet("background-color: #333;")

        # Simple layout with button bar and video frame
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        
        self.button_bar = QHBoxLayout()
        self.external_btn = QPushButton("Open in New Window")
        self.button_bar.addWidget(self.external_btn)
        
        layout.addLayout(self.button_bar)
        layout.addWidget(self.video_frame, 1)  # Give video frame stretch priority
        
        self.external_btn.clicked.connect(self.open_new_window)
        self.current_url = None

        # Set minimum size with 16:9 ratio
        self.setMinimumWidth(400)
        self.setMinimumHeight(int(400 * 9/16) + 40)  # Add space for button

    def play_url(self, url):
        if not vlc:
            logging.warning("VLC is not available, cannot play URL.")
            return
        
        logging.info(f"Attempting to play URL in embedded player: {url}")
        VLCManager.kill_existing()
        media = self.instance.media_new(url)
        self.player.set_media(media)
        
        if sys.platform.startswith("linux"):
            self.player.set_xwindow(self.video_frame.winId())
            logging.info(f"Using xwindow ID: {self.video_frame.winId()}")
        else:
            self.player.set_hwnd(self.video_frame.winId())
            logging.info(f"Using hwnd ID: {self.video_frame.winId()}")
        
        if not self.video_frame.winId():
            logging.error("Invalid video frame window ID. VLC may not display correctly.")
        
        self.player.play()
        self.current_url = url  # Store the current URL
        logging.info("VLC player started.")

    def open_new_window(self):
        if not vlc:
            return
        if self.current_url:
            self.player.stop()
            VLCManager.play_url(self.current_url)  # Use the stored URL
        else:
            logging.warning("No URL to open in new window.")

    def stop(self):
        if vlc:
            self.player.stop()

    def resizeEvent(self, event):
        """Keep widget height in sync with width for 16:9 ratio."""
        width = event.size().width()
        # Calculate desired height (16:9 ratio plus button space)
        height = int(width * 9/16) + 40  # Add space for button
        if height != event.size().height():
            self.setFixedHeight(height)
        super().resizeEvent(event)
