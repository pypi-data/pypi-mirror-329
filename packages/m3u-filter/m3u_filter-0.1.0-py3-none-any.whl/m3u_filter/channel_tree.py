from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView, QMenu, QAction, QApplication
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen
import os, hashlib, requests, threading
from m3u_filter.vlc_manager import VLCManager
import logging
from m3u_filter.icon_cache import fetch_icon
import json
import unicodedata

class ChannelTree(QTreeWidget):
    channelSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.checked_groups = set()
        self.checked_channels = set()
        self.stored_group_states = {}  # Store states when group becomes fully checked
        self.setup_clear_icon()
        self.setup_ui()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        logging.debug("ChannelTree initialized")
        self.blockSignals(False)  # Make sure signals aren't blocked
        self.current_entries = []  # Add this to store current entries
        self.load_icons = True  # Default to loading icons

    def setup_clear_icon(self):
        # Create a red cross icon
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.red, 2))
        painter.drawLine(4, 4, 12, 12)
        painter.drawLine(4, 12, 12, 4)
        painter.end()
        self.clear_icon = QIcon(pixmap)

    def setup_ui(self):
        self.setColumnCount(5)  # Back to 5 columns
        self.setHeaderLabels(["", "Group", "Logo", "Channel", "URL"])
        self.setIconSize(QSize(48, 48))
        self.itemChanged.connect(self.on_checkbox_changed)
        self.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.itemClicked.connect(self.on_item_clicked)
        logging.debug("ChannelTree UI setup complete")

    def populate(self, entries):
        self.current_entries = entries
        self.clear()
        groups = {}
        
        # Determine whether to load icons based on entry count
        self.load_icons = len(entries) <= 300
        self.setColumnHidden(2, not self.load_icons)

        # Debug current state
        logging.debug(f"Populating tree with checked_channels: {len(self.checked_channels)}")
        logging.debug(f"Checked groups: {self.checked_groups}")

        for entry in entries:
            group_name = entry["group"]
            if group_name not in groups:
                group_item = QTreeWidgetItem()
                group_item.setText(1, group_name)
                group_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable)
                group_item.setCheckState(0, Qt.Checked if group_name in self.checked_groups else Qt.Unchecked)
                group_item.setIcon(0, self.clear_icon)
                groups[group_name] = group_item
                self.addTopLevelItem(group_item)
            
            group_item = groups[group_name]
            child = QTreeWidgetItem()
            child.setText(3, entry["name"])
            child.setText(4, entry["url"])
            child.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable)
            
            # Just check if URL is in checked_channels, nothing else
            is_checked = entry["url"] in self.checked_channels
            child.setCheckState(0, Qt.Checked if is_checked else Qt.Unchecked)
            logging.debug(f"Channel '{entry['name']}' checked state: {is_checked}")
            
            if self.load_icons:
                icon = fetch_icon(entry["logo"], 
                    lambda icon, item=child: item.setIcon(2, icon))
                if icon:
                    child.setIcon(2, icon)
            
            group_item.addChild(child)

        # Auto-resize columns
        header = self.header()
        for i in range(5):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        # Hide the URL column
        self.setColumnHidden(4, True)

    def update_group_state(self, group_item):
        total = group_item.childCount()
        checked = sum(
            group_item.child(i).checkState(0) == Qt.Checked 
            for i in range(total)
        )
        if checked == 0:
            group_item.setCheckState(0, Qt.Unchecked)
        elif checked == total:
            group_item.setCheckState(0, Qt.Checked)
        else:
            group_item.setCheckState(0, Qt.PartiallyChecked)

    def on_checkbox_changed(self, item, column):
        if column == 0:
            self.blockSignals(True)
            is_checked = item.checkState(0) == Qt.Checked
            
            if item.parent() is None:  # Group item
                group_name = item.text(1)
                
                if is_checked:
                    # Store current state before checking all
                    self.stored_group_states[group_name] = {
                        item.child(i).text(4)
                        for i in range(item.childCount())
                        if item.child(i).checkState(0) == Qt.Checked
                    }
                    
                    # Check all channels
                    self.checked_groups.add(group_name)
                    for i in range(item.childCount()):
                        child = item.child(i)
                        child.setCheckState(0, Qt.Checked)
                        self.checked_channels.add(child.text(4))
                else:
                    # Restore previous state if it exists
                    self.checked_groups.discard(group_name)
                    stored_state = self.stored_group_states.get(group_name, set())
                    
                    for i in range(item.childCount()):
                        child = item.child(i)
                        url = child.text(4)
                        was_checked = url in stored_state
                        child.setCheckState(0, Qt.Checked if was_checked else Qt.Unchecked)
                        if was_checked:
                            self.checked_channels.add(url)
                        else:
                            self.checked_channels.discard(url)
                    
                    # Update group state to show partial if needed
                    self.update_group_state(item)
                    if item.checkState(0) == Qt.Checked:
                        self.checked_groups.add(group_name)
                    # Note: we don't need an else here as we already discarded above
                
                logging.debug(f"Group '{group_name}' checked state: {is_checked}")
                logging.debug(f"Stored states: {self.stored_group_states}")
                
            else:  # Channel item
                url = item.text(4)
                parent = item.parent()
                group_name = parent.text(1)
                
                if is_checked:
                    self.checked_channels.add(url)
                else:
                    self.checked_channels.discard(url)
                
                # Update parent group state
                all_checked = all(parent.child(i).checkState(0) == Qt.Checked 
                                for i in range(parent.childCount()))
                any_checked = any(parent.child(i).checkState(0) == Qt.Checked 
                                for i in range(parent.childCount()))
                
                if all_checked:
                    parent.setCheckState(0, Qt.Checked)
                    self.checked_groups.add(group_name)
                    # Store the current state as it's fully checked
                    self.stored_group_states[group_name] = self.checked_channels.copy()
                elif any_checked:
                    parent.setCheckState(0, Qt.PartiallyChecked)
                    self.checked_groups.discard(group_name)
                    # Forget stored state as we have a partial selection
                    if group_name in self.stored_group_states:
                        del self.stored_group_states[group_name]
                else:
                    parent.setCheckState(0, Qt.Unchecked)
                    self.checked_groups.discard(group_name)
                    # Forget stored state as nothing is selected
                    if group_name in self.stored_group_states:
                        del self.stored_group_states[group_name]
                
                logging.debug(f"Channel '{item.text(3)}' checked state: {is_checked}")
                logging.debug(f"Stored group states: {self.stored_group_states}")

            self.blockSignals(False)

    def on_item_double_clicked(self, item, column):
        if item.parent() is not None and column == 4:
            url = item.text(4)
            VLCManager.play_url(url)

    def on_item_clicked(self, item, column):
        if item.parent() is None:  # Group item
            icon_rect = self.visualItemRect(item)
            # Check if click is in the icon area of the first column
            if column == 0 and icon_rect.x() + 16 <= self.clickedPos.x() <= icon_rect.x() + 32:
                self.clear_group_selections(item)
            elif column > 0:  # Keep existing expand/collapse behavior
                item.setExpanded(not item.isExpanded())
        elif column in (2, 3):  # Channel item, logo or name column
            url = item.text(4)
            logging.info(f"Channel selected, emitting URL: {url}")
            self.channelSelected.emit(url)

    def mousePressEvent(self, event):
        self.clickedPos = event.pos()
        super().mousePressEvent(event)

    def clear_group_selections(self, group_item):
        """Toggle between clearing all selections and restoring previous state."""
        group_name = group_item.text(1)
        logging.debug(f"Toggling clear selections for group: {group_name}")
        
        # Block signals during our changes
        self.blockSignals(True)
        
        # Check if any channels are currently checked or if group is partially checked
        any_selected = (any(
            group_item.child(i).checkState(0) == Qt.Checked
            for i in range(group_item.childCount())
        ) or group_item.checkState(0) == Qt.PartiallyChecked)
        
        if any_selected:
            # Store current state and clear everything
            self.stored_group_states[group_name] = {
                group_item.child(i).text(4)
                for i in range(group_item.childCount())
                if group_item.child(i).checkState(0) == Qt.Checked
            }
            logging.debug(f"Stored state for {group_name}: {self.stored_group_states[group_name]}")
            
            # Clear all selections
            for i in range(group_item.childCount()):
                child = group_item.child(i)
                child.setCheckState(0, Qt.Unchecked)
                self.checked_channels.discard(child.text(4))
            
            group_item.setCheckState(0, Qt.Unchecked)
            self.checked_groups.discard(group_name)
            logging.debug("Cleared all selections")
            
        else:
            # Try to restore previous state
            if group_name in self.stored_group_states:
                stored_state = self.stored_group_states[group_name]
                logging.debug(f"Restoring state: {stored_state}")
                
                # Restore all channel states
                for i in range(group_item.childCount()):
                    child = group_item.child(i)
                    url = child.text(4)
                    was_checked = url in stored_state
                    child.setCheckState(0, Qt.Checked if was_checked else Qt.Unchecked)
                    if was_checked:
                        self.checked_channels.add(url)
                    else:
                        self.checked_channels.discard(url)
                
                # Update group state immediately
                self.update_group_state(group_item)
                if group_item.checkState(0) == Qt.Checked:
                    self.checked_groups.add(group_name)
                else:
                    self.checked_groups.discard(group_name)
                    
                logging.debug(f"Restored state with group state: {group_item.checkState(0)}")
            else:
                logging.debug(f"No previous state found for group: {group_name}")
        
        self.blockSignals(False)

    def get_selected_entries(self, all_entries):
        return [
            e for e in all_entries 
            if (e["url"] in self.checked_channels) or (e["group"] in self.checked_groups)
        ]

    def show_context_menu(self, pos):
        item = self.itemAt(pos)
        if not item or item.parent() is None:
            return  # Only show menu for channel items
        menu = QMenu(self)
        copy_url_action = QAction("Copy URL", self)
        url = item.text(4)
        copy_url_action.triggered.connect(lambda: QApplication.clipboard().setText(url))
        menu.addAction(copy_url_action)
        menu.exec_(self.mapToGlobal(pos))

    def apply_filter_state(self, state):
        """Apply a saved filter state."""
        logging.debug(f"Applying filter state: {state}")

        # Handle groups
        self.checked_groups = set(state.get("groups", []))

        # Create lookup for current entries
        entries_by_id = {}
        group_counts = {}  # Track how many channels are in each group
        for entry in self.current_entries:
            entry_id = (entry["group"], entry["name"])
            entries_by_id[entry_id] = entry
            group_counts[entry["group"]] = group_counts.get(entry["group"], 0) + 1

        # Reset checked channels
        self.checked_channels = set()

        # Add channels from checked groups
        channels_from_groups = 0
        for entry in self.current_entries:
            if entry["group"] in self.checked_groups:
                self.checked_channels.add(entry["url"])
                channels_from_groups += 1

        # Add individually checked channels by matching group+name
        channels_from_individual = 0
        for channel in state.get("channels", []):
            channel_id = (channel["group"], channel["name"])
            if channel_id in entries_by_id:
                entry = entries_by_id[channel_id]
                if entry["url"] not in self.checked_channels:
                    self.checked_channels.add(entry["url"])
                    channels_from_individual += 1

        # Clear stored states and refresh display
        self.stored_group_states = {}
        self.populate(self.current_entries)

        # This needs to reflect the total number of selected channels
        total_channels = len(self.checked_channels)
        logging.info(f"Applied filter: {len(self.checked_groups)} groups ({channels_from_groups} channels) + "
                    f"{channels_from_individual} individual channels = {total_channels} total")

    def get_filter_state(self):
        """Export the current filter state."""
        # Create lookup from URL to entry
        url_to_entry = {e["url"]: e for e in self.current_entries}

        # Get individually checked channels (not part of fully checked groups)
        individual_channels = []
        for url in self.checked_channels:
            entry = url_to_entry.get(url)
            if entry and entry["group"] not in self.checked_groups:
                individual_channels.append({
                    "name": entry["name"],
                    "group": entry["group"]
                })
            else:
                logging.debug(f"Skipping {url} because it is in a checked group")

        logging.info(f"Number of individual channels: {len(individual_channels)}")
        return {
            "groups": list(self.checked_groups),
            "channels": individual_channels
        }

    def normalize_string(self, s):
        """Normalize Unicode strings for comparison using standard NFKC normalization."""
        return s # Do nothing
