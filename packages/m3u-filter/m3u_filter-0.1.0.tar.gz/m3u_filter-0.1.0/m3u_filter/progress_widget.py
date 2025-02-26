from PyQt5.QtWidgets import QProgressBar, QWidget, QHBoxLayout
from PyQt5.QtCore import QTimer

class ProgressWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        
        self._progress = QProgressBar()
        self._layout.addWidget(self._progress)
        self._progress.setMaximum(100)
        self.hide()
        self._hide_timer = None

    def layout(self):
        return self._layout

    def clear_extra_widgets(self):
        """Remove all widgets except the progress bar."""
        for i in reversed(range(self._layout.count())):
            item = self._layout.itemAt(i)
            if item.widget() != self._progress:
                item.widget().deleteLater()
                self._layout.removeItem(item)

    # Delegate all progress bar methods to self._progress
    def start_progress(self, format_str=""):
        self.clear_extra_widgets()  # Clear any existing buttons
        self._progress.setValue(0)
        if format_str:
            self._progress.setFormat(format_str)
        self.show()

    def update_progress(self, value, format_str=None):
        self._progress.setValue(value)
        if format_str is not None:
            self._progress.setFormat(format_str)

    def finish(self, format_str="Done", hide_after_ms=5000):
        """Show completion and optionally hide after delay."""
        self._progress.setValue(100)
        self._progress.setFormat(format_str)
        
        # Cancel any existing hide timer
        if self._hide_timer:
            self._hide_timer.stop()
        
        if hide_after_ms > 0:
            self._hide_timer = QTimer()
            self._hide_timer.setSingleShot(True)
            self._hide_timer.timeout.connect(self.hide)
            self._hide_timer.start(hide_after_ms)

    def processing(self, format_str="Processing...", value=95):
        """Show indeterminate progress for processing stage."""
        self._progress.setValue(value)
        self._progress.setFormat(format_str)
