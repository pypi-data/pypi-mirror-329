#!/usr/bin/env python3
import sys
import logging
import subprocess
import pkg_resources
from PyQt5.QtWidgets import QApplication
from m3u_filter.gui import MainWindow   # Correct namespace

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,  # Changed from DEBUG to INFO
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('m3u_filter.log')
        ]
    )

def check_dependencies():
    """Check if all required packages are installed."""
    required = {'pyqt5', 'requests', 'python-vlc', 'psutil'}  # Changed PyQt5 to pyqt5
    installed = {pkg.key.lower() for pkg in pkg_resources.working_set}  # Convert to lowercase
    missing = required - installed
    
    if missing:
        print("Error: Missing required packages:", ", ".join(missing))
        print("\nPlease install them using:")
        print(f"pip install {' '.join(missing)}")
        return False
    return True

def main():
    setup_logging()
    logging.info("Starting M3U Filter application")
    
    if not check_dependencies():
        sys.exit(1)
    
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Application error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
