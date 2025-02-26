from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QFileDialog, QLineEdit, QLabel, QMessageBox, QProgressBar
)
from PyQt5.QtCore import QSettings, QTimer
from m3u_filter.m3u_handler import download_m3u_xtream, parse_m3u, create_m3u_content
from m3u_filter.channel_tree import ChannelTree
import json
import requests
from m3u_filter.embedded_vlc import EmbeddedVLC
import logging
import os
from m3u_filter.progress_widget import ProgressWidget
from m3u_filter.download_worker import DownloadWorker
from PyQt5.QtCore import QThread
from m3u_filter.m3u_downloader import M3UDownloader
from m3u_filter.m3u_server import M3UServer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.checked_groups = set()
        self.checked_channels = set()
        self.vlc_widget = EmbeddedVLC()  # Initialize vlc_widget here
        self.init_ui()
        self.load_saved_content()
        self.tree_widget.channelSelected.connect(self.on_channel_selected)
        self.downloader = M3UDownloader(self)
        self.server = M3UServer()

    def get_source_description(self):
        """Get a human-readable description of the current source."""
        source = self.last_import.get("source", "")
        params = self.last_import.get("params", {})
        
        if source == "m3u_url":
            return f"URL: {params.get('url', 'Not set')}"
        elif source == "xtream":
            return f"Xtream: {params.get('base', 'Not set')}"
        elif source == "file":
            return f"File: {params.get('file', 'Not set')}"
        return "No source configured"

    def update_source_description(self):
        """Update the source description label."""
        self.source_description.setText(self.get_source_description())

    def init_ui(self):
        self.setWindowTitle("M3U Filter")
        self.setGeometry(100, 100, 1200, 800)
        self.settings = QSettings("ko_dez", "M3UFilter")
        
        main_layout = QVBoxLayout()
        
        # Top area: search
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search groups and channels...")
        self.search_input.textChanged.connect(self.apply_filter)
        self.clear_search_button = QPushButton("Clear")
        self.clear_search_button.clicked.connect(self.clear_search)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.clear_search_button)
        main_layout.addLayout(search_layout)
        
        # Main content area with tree and right panel
        main_split = QHBoxLayout()
        
        # Left side: Channel tree (stretch=1)
        self.tree_widget = ChannelTree()
        main_split.addWidget(self.tree_widget, stretch=1)
        
        # Right side panel (no stretch to keep natural width)
        right_panel = QVBoxLayout()
        
        # Source controls section
        source_section = QVBoxLayout()
        source_button = QPushButton("Source Settings")
        source_button.clicked.connect(self.import_m3u)
        source_section.addWidget(source_button)
        
        # Source info and reload
        source_info = QHBoxLayout()
        self.source_description = QLabel("No source configured")
        self.source_description.setWordWrap(True)
        source_info.addWidget(self.source_description, stretch=1)
        
        reload_button = QPushButton("↻")
        reload_button.setToolTip("Reload from source")
        reload_button.clicked.connect(self.reload_m3u)
        reload_button.setMaximumWidth(30)
        source_info.addWidget(reload_button)
        source_section.addLayout(source_info)
        right_panel.addLayout(source_section)
        
        # Tree control buttons
        self.collapse_all_button = QPushButton("Collapse All")
        self.collapse_all_button.clicked.connect(self.tree_widget.collapseAll)
        right_panel.addWidget(self.collapse_all_button)
        
        self.expand_all_button = QPushButton("Expand All")
        self.expand_all_button.clicked.connect(self.tree_widget.expandAll)
        right_panel.addWidget(self.expand_all_button)
        
        self.show_selected_button = QPushButton("Show Selected Only")
        self.show_selected_button.clicked.connect(self.show_selected_only)
        right_panel.addWidget(self.show_selected_button)
        
        self.show_all_button = QPushButton("Show All")
        self.show_all_button.clicked.connect(lambda: self.tree_widget.populate(self.m3u_content))
        right_panel.addWidget(self.show_all_button)
        
        # Replace single save button with two export buttons
        export_layout = QHBoxLayout()
        self.export_selected_button = QPushButton("Export Selected")
        self.export_all_button = QPushButton("Export All")
        self.export_selected_button.clicked.connect(lambda: self.export_m3u(selected_only=True))
        self.export_all_button.clicked.connect(lambda: self.export_m3u(selected_only=False))
        export_layout.addWidget(self.export_selected_button)
        export_layout.addWidget(self.export_all_button)
        right_panel.addLayout(export_layout)
        
        self.load_filter_button = QPushButton("Load Filter")
        self.load_filter_button.clicked.connect(self.load_filter)
        right_panel.addWidget(self.load_filter_button)
        
        # Add server controls before the load filter button
        server_layout = QHBoxLayout()
        self.server_port = QLineEdit()
        self.server_port.setPlaceholderText("Port (default: 4567)")
        self.server_port.setMaximumWidth(100)
        self.server_toggle = QPushButton("Start Server")
        self.server_toggle.setCheckable(True)
        self.server_toggle.clicked.connect(self.toggle_server)
        server_layout.addWidget(self.server_port)
        server_layout.addWidget(self.server_toggle)
        right_panel.addLayout(server_layout)

        # Add stretch to push VLC to bottom
        right_panel.addStretch()
        
        # VLC section at bottom
        width = 400
        height = int(width * 9/16)
        self.vlc_widget.setFixedSize(width, height)
        
        self.progress = ProgressWidget()
        right_panel.addWidget(self.progress)
        right_panel.addWidget(self.vlc_widget)
        
        # VLC controls below video
        vlc_controls = QHBoxLayout()
        external_btn = QPushButton("Open in New Window")
        external_btn.clicked.connect(self.vlc_widget.open_new_window)
        vlc_controls.addWidget(external_btn)
        right_panel.addLayout(vlc_controls)
        
        # Add right panel to main split
        right_container = QWidget()
        right_container.setLayout(right_panel)
        right_container.setFixedWidth(width + 20)  # VLC width + margin
        main_split.addWidget(right_container)
        
        # Finish layout
        main_layout.addLayout(main_split)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        self.m3u_raw = ""
        self.m3u_content = []
        self.last_import = {}

    def load_saved_content(self):
        last_m3u = self.settings.value("last_m3u", "")
        last_import = self.settings.value("last_import", "")
        if last_import:
            try:
                self.last_import = json.loads(last_import)
                self.update_source_description()
            except json.JSONDecodeError:
                self.last_import = {}
        
        if last_m3u:
            self.m3u_raw = last_m3u
            self.m3u_content = parse_m3u(last_m3u)
            self.tree_widget.populate(self.m3u_content)

    def reload_m3u(self):
        """Central function to load/reload M3U content from the current source."""
        if not self.last_import:
            return
            
        # Restore categories if they were saved
        categories = set(self.last_import.get("categories", ["livetv"]))
        
        def on_complete(content):
            self.m3u_raw = content
            self.progress.start_progress("Parsing M3U file...")
            
            def on_progress(value):
                self.progress.update_progress(value)
                
            self.m3u_content = parse_m3u(self.m3u_raw, progress_callback=on_progress)
            self.progress.processing("Rendering list...")
            self.tree_widget.populate(self.m3u_content)
            self.progress.finish("Done")
            
            # Save the successfully loaded content
            self.settings.setValue("last_m3u", self.m3u_raw)
            self.settings.setValue("last_import", json.dumps(self.last_import))
            
        self.downloader.start_download(
            self.last_import.get("source", ""),
            self.last_import.get("params", {}),
            categories,  # Add categories parameter
            self.progress,
            on_complete
        )

    def import_m3u(self):
        """Just collect and save source parameters, then reload."""
        from import_source_dialog import ImportSourceDialog
        dialog = ImportSourceDialog(self)
        if dialog.exec_():
            # Save the new source info including categories
            self.last_import = {
                "source": dialog.source,
                "params": dialog.params,
                "categories": list(dialog.selected_categories)  # Add this line
            }
            self.settings.setValue("last_import", json.dumps(self.last_import))
            self.update_source_description()
            
            # Use the common reload function
            self.reload_m3u()

    def apply_filter(self):
        search_text = self.search_input.text().lower()
        if (search_text):
            filtered_entries = [
                e for e in self.m3u_content 
                if search_text in e["name"].lower() or search_text in e["group"].lower()
            ]
            self.tree_widget.populate(filtered_entries)
            self.tree_widget.expandAll()

    def clear_search(self):
        self.search_input.clear()
        self.tree_widget.populate(self.m3u_content)

    def show_selected_only(self):
        filtered_entries = self.tree_widget.get_selected_entries(self.m3u_content)
        self.tree_widget.populate(filtered_entries)
        self.tree_widget.expandAll()
        # Optional: stop VLC if desired
        if self.vlc_widget:
            self.vlc_widget.stop()

    def export_m3u(self, selected_only=True):
        """Export M3U content to a file."""
        # Get entries to save
        if selected_only:
            entries = self.tree_widget.get_selected_entries(self.m3u_content)
            if not entries:
                QMessageBox.warning(self, "No Selection", 
                                  "No channels are selected. Please select some channels first.")
                return
        else:
            entries = self.m3u_content

        # Get last directory from settings or default to home
        last_dir = self.settings.value("last_save_directory", os.path.expanduser("~"))
        
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Export Selected Channels" if selected_only else "Export All Channels",
            last_dir,
            "M3U Files (*.m3u);;All Files (*)",
            options=options
        )
        
        if file_path:
            # Add .m3u extension if missing
            if not file_path.lower().endswith('.m3u'):
                file_path += '.m3u'
            
            # Save the directory for next time
            self.settings.setValue("last_save_directory", os.path.dirname(file_path))
            
            try:
                # Save M3U content
                content = create_m3u_content(entries)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                # Save filter state only for selected exports
                if selected_only:
                    filter_path = file_path + '.filter'
                    filter_state = self.tree_widget.get_filter_state()
                    with open(filter_path, 'w', encoding='utf-8') as file:
                        json.dump(filter_state, file, indent=2, ensure_ascii=False)
                    
                    QMessageBox.information(
                        self, "Success", 
                        f"Saved {len(entries)} channels to {file_path}\n"
                        f"Filter state saved to {os.path.basename(filter_path)}"
                    )
                else:
                    QMessageBox.information(
                        self, "Success", 
                        f"Exported {len(entries)} channels to {file_path}"
                    )
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", 
                    f"Failed to save files: {str(e)}"
                )

    def load_filter(self):
        """Load a filter file and apply it."""
        options = QFileDialog.Options()
        last_dir = self.settings.value("last_save_directory", os.path.expanduser("~"))
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Filter", 
            last_dir,
            "Filter Files (*.filter);;All Files (*)",
            options=options
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    filter_state = json.load(file)
                self.tree_widget.apply_filter_state(filter_state)
                QMessageBox.information(
                    self, "Success", 
                    f"Filter loaded from {os.path.basename(file_path)}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", 
                    f"Failed to load filter: {str(e)}"
                )

    def toggle_server(self):
        if self.server.is_running():
            self.server.stop()
            self.server_toggle.setText("Start Server")
            self.server_toggle.setChecked(False)
            self.server_port.setEnabled(True)
        else:
            try:
                port = int(self.server_port.text()) if self.server_port.text() else 4567
                self.server = M3UServer(port)
                # Serve only selected channels
                self.server.set_content_callback(
                    lambda: create_m3u_content(self.tree_widget.get_selected_entries(self.m3u_content))
                )
                if self.server.start():
                    self.server_toggle.setText("Stop Server")
                    self.server_toggle.setChecked(True)
                    self.server_port.setEnabled(False)
                else:
                    self.server_toggle.setChecked(False)
                    QMessageBox.critical(self, "Error", f"Failed to start server on port {port}")
            except ValueError:
                QMessageBox.warning(self, "Invalid Port", "Please enter a valid port number")
                self.server_toggle.setChecked(False)

    def closeEvent(self, event):
        """Clean up server when closing."""
        if self.server:
            self.server.stop()
        super().closeEvent(event)

    def on_channel_selected(self, url):
        logging.info(f"Received channelSelected signal with URL: {url}")
        if self.vlc_widget and self.vlc_widget.isEnabled():
            logging.info("Calling vlc_widget.play_url")
            self.vlc_widget.play_url(url)
        else:
            logging.warning("VLC widget is not available or disabled.")
