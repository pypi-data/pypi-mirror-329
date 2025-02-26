import json
import os
import urllib.parse
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget,
    QWidget, QLineEdit, QLabel, QDialogButtonBox, QFileDialog, QMessageBox
)
from m3u_filter.m3u_downloader import M3UDownloader

class ImportSourceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("M3U Source Settings")
        self.setMinimumWidth(400)
        
        self.settings = QSettings("ko_dez", "M3UFilter")
        self.load_last_import()
        self.setup_ui()
        
        self.source = ""
        self.params = {}
        self.selected_categories = {"livetv"}  # default to only Live TV

    def load_last_import(self):
        """Load and parse the last import settings."""
        last_import_json = self.settings.value("last_import", "")
        try:
            self.last_import = json.loads(last_import_json) if last_import_json else {}
        except json.JSONDecodeError:
            self.last_import = {}

    def setup_ui(self):
        """Initialize all UI elements."""
        self.layout = QVBoxLayout(self)
        self.setup_source_buttons()
        self.setup_stacked_widget()
        self.setup_dialog_buttons()
        
        # Category checkboxes
        cat_layout = QHBoxLayout()
        self.live_checkbox = QPushButton("Live TV")
        self.live_checkbox.setCheckable(True)
        self.live_checkbox.setChecked(True)  # Only Live TV is selected by default

        self.movie_checkbox = QPushButton("Movies")
        self.movie_checkbox.setCheckable(True)
        self.movie_checkbox.setChecked(False)  # Uncheck by default

        self.series_checkbox = QPushButton("Series")
        self.series_checkbox.setCheckable(True)
        self.series_checkbox.setChecked(False)  # Uncheck by default

        self.live_checkbox.clicked.connect(self.update_categories)
        self.movie_checkbox.clicked.connect(self.update_categories)
        self.series_checkbox.clicked.connect(self.update_categories)
        cat_layout.addWidget(self.live_checkbox)
        cat_layout.addWidget(self.movie_checkbox)
        cat_layout.addWidget(self.series_checkbox)
        self.layout.addLayout(cat_layout)
        
        # Restore category selections from last import
        if "categories" in self.last_import:
            self.selected_categories = set(self.last_import["categories"])
            self.live_checkbox.setChecked("livetv" in self.selected_categories)
            self.movie_checkbox.setChecked("movie" in self.selected_categories)
            self.series_checkbox.setChecked("series" in self.selected_categories)
        else:
            # Default to only Live TV
            self.selected_categories = {"livetv"}
            self.live_checkbox.setChecked(True)
            self.movie_checkbox.setChecked(False)
            self.series_checkbox.setChecked(False)

    def setup_source_buttons(self):
        """Setup the source selection buttons."""
        self.button_layout = QHBoxLayout()
        self.url_button = QPushButton("M3U URL")
        self.xtream_button = QPushButton("Xtream")
        self.file_button = QPushButton("File")
        
        for btn in [self.url_button, self.xtream_button, self.file_button]:
            btn.setCheckable(True)
            self.button_layout.addWidget(btn)
        
        self.layout.addLayout(self.button_layout)
        self.select_initial_source()
        
        self.url_button.clicked.connect(lambda: self.select_source(0))
        self.xtream_button.clicked.connect(lambda: self.select_source(1))
        self.file_button.clicked.connect(lambda: self.select_source(2))

    def select_initial_source(self):
        """Select the initial source based on last import settings."""
        source = self.last_import.get("source", "m3u_url")
        if source == "m3u_url":
            self.selected_index = 0
            self.url_button.setChecked(True)
        elif source == "xtream":
            self.selected_index = 1
            self.xtream_button.setChecked(True)
        elif source == "file":
            self.selected_index = 2
            self.file_button.setChecked(True)
        else:
            self.selected_index = 0
            self.url_button.setChecked(True)

    def setup_stacked_widget(self):
        """Setup the stacked widget with different source options."""
        self.stacked = QStackedWidget(self)
        # Page 0 - M3U URL
        page0 = QWidget()
        p0_layout = QVBoxLayout(page0)
        self.url_edit = QLineEdit()
        p0_layout.addWidget(QLabel("M3U URL:"))
        p0_layout.addWidget(self.url_edit)
        self.stacked.addWidget(page0)
        # Page 1 - Xtream
        page1 = QWidget()
        p1_layout = QVBoxLayout(page1)
        self.xtream_base = QLineEdit()
        self.xtream_username = QLineEdit()
        self.xtream_password = QLineEdit()
        p1_layout.addWidget(QLabel("Xtream Base URL:"))
        p1_layout.addWidget(self.xtream_base)
        p1_layout.addWidget(QLabel("Username:"))
        p1_layout.addWidget(self.xtream_username)
        p1_layout.addWidget(QLabel("Password:"))
        p1_layout.addWidget(self.xtream_password)
        self.stacked.addWidget(page1)
        # Page 2 - File
        page2 = QWidget()
        p2_layout = QVBoxLayout(page2)
        self.file_edit = QLineEdit()
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_file)
        p2_layout.addWidget(QLabel("File Path:"))
        p2_layout.addWidget(self.file_edit)
        p2_layout.addWidget(browse_btn)
        self.stacked.addWidget(page2)

        self.layout.addWidget(self.stacked)
        self.stacked.setCurrentIndex(self.selected_index)
        
        # Pre-populate fields if last_import exists.
        source = self.last_import.get("source", "m3u_url")
        if source == "m3u_url":
            url = self.last_import.get("params", {}).get("url", "")
            self.url_edit.setText(url)
        elif source == "xtream":
            params = self.last_import.get("params", {})
            self.xtream_base.setText(params.get("base", ""))
            self.xtream_username.setText(params.get("username", ""))
            self.xtream_password.setText(params.get("password", ""))
        elif source == "file":
            file_path = self.last_import.get("params", {}).get("file", "")
            self.file_edit.setText(file_path)

    def setup_dialog_buttons(self):
        """Setup the dialog buttons."""
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.load_m3u)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def select_source(self, index):
        self.selected_index = index
        self.stacked.setCurrentIndex(index)
        self.url_button.setChecked(index == 0)
        self.xtream_button.setChecked(index == 1)
        self.file_button.setChecked(index == 2)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select M3U File", "", "M3U Files (*.m3u);;All Files (*)")
        if file_path:
            self.file_edit.setText(file_path)

    def update_categories(self):
        """Sync the selected categories with checkbox states."""
        self.selected_categories.clear()
        if self.live_checkbox.isChecked():
            self.selected_categories.add("livetv")
        if self.movie_checkbox.isChecked():
            self.selected_categories.add("movie")
        if self.series_checkbox.isChecked():
            self.selected_categories.add("series")

    def load_m3u(self):
        """Validate input and start async download."""
        try:
            if self.selected_index == 0:  # m3u_url
                url = self.url_edit.text().strip()
                if not url:
                    QMessageBox.warning(self, "Error", "Please enter a valid URL")
                    return
                self.source = "m3u_url"
                self.params = {"url": url}
            elif self.selected_index == 1:  # Xtream
                base = self.xtream_base.text().strip()
                user = self.xtream_username.text().strip()
                pwd = self.xtream_password.text().strip()
                if not (base and user and pwd):
                    QMessageBox.warning(self, "Error", "Please fill in Xtream credentials.")
                    return
                self.source = "xtream"
                self.params = {"base": base, "username": user, "password": pwd}
            else:  # File
                file_path = self.file_edit.text().strip()
                if not file_path or not os.path.exists(file_path):
                    QMessageBox.warning(self, "Error", "Please select a valid file")
                    return
                self.source = "file"
                self.params = {"file": file_path}

            # Save source info and categories
            self.parent().last_import = {
                "source": self.source,
                "params": self.params,
                "categories": list(self.selected_categories)
            }
            self.settings.setValue("last_import", 
                json.dumps(self.parent().last_import))
            
            # Start download
            def on_complete(content):
                self.accept()

            self.parent().downloader.start_download(
                self.source,
                self.params,
                self.selected_categories,  # Pass categories directly to download
                self.parent().progress,
                on_complete
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load M3U: {str(e)}")
            self.reject()
