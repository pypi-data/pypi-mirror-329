import psutil
import subprocess
import logging

class VLCManager:
    @staticmethod
    def kill_existing():
        """Kill all running VLC instances."""
        killed = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower().startswith('vlc'):
                    logging.info(f"Killing VLC process: {proc.info['pid']}")
                    proc.kill()
                    killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        if not killed:
            logging.info("No existing VLC processes found.")

    @staticmethod
    def play_url(url):
        """Kill existing VLC instances and play the given URL."""
        logging.info(f"Attempting to play URL in external VLC: {url}")
        try:
            VLCManager.kill_existing()
            subprocess.Popen(['vlc', url])
        except Exception as e:
            logging.error(f"Failed to open VLC: {str(e)}")
