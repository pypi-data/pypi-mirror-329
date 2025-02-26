from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import logging
from m3u_filter.m3u_handler import download_m3u_xtream  # correct reference

class M3URequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """Override to use our logging with better encoding handling."""
        try:
            logging.info(f"M3U Server: {format%args}")
        except UnicodeEncodeError:
            # Fallback for binary/SSL requests
            logging.info("M3U Server: Received binary/SSL request (not supported)")

    def handle_one_request(self):
        """Override to handle SSL requests gracefully."""
        try:
            return super().handle_one_request()
        except ValueError:
            # This is likely an SSL request
            self.raw_requestline = self.rfile.readline()
            if not self.raw_requestline:
                self.close_connection = True
                return
            
            self.send_error(400, "SSL/HTTPS not supported. Please use HTTP.")
        except Exception as e:
            logging.error(f"Error handling request: {str(e)}")
            self.send_error(500, "Internal server error")

    def do_GET(self):
        """Handle all GET requests by returning the M3U content."""
        try:
            content = self.server.get_content()
            # Convert content to bytes with explicit encoding
            content_bytes = content.encode('utf-8')
            
            self.send_response(200)
            self.send_header('Content-Type', 'audio/x-mpegurl; charset=utf-8')
            self.send_header('Content-Length', str(len(content_bytes)))
            self.end_headers()
            
            # Write all content at once, not in chunks
            self.wfile.write(content_bytes)
            self.wfile.flush()
            
        except (BrokenPipeError, ConnectionError) as e:
            logging.warning(f"Client disconnected: {e}")
        except Exception as e:
            logging.error(f"Error serving M3U: {e}")
            self.send_error(500, str(e))

class M3UServer:
    def __init__(self, port=4567):
        self.port = port
        self.server = None
        self.thread = None
        self._get_content = lambda: "#EXTM3U\n"  # Default empty playlist

    def set_content_callback(self, callback):
        """Store callback so it can be applied when server is running."""
        self._get_content = callback
        if self.server:
            self.server.get_content = self._get_content

    def start(self):
        """Start the server in a background thread."""
        if self.server:
            return

        class M3UHTTPServer(HTTPServer):
            get_content = self._get_content

        try:
            self.server = M3UHTTPServer(('', self.port), M3URequestHandler)
            self.server.get_content = self._get_content
            self.thread = threading.Thread(target=self.server.serve_forever)
            self.thread.daemon = True
            self.thread.start()
            logging.info(f"M3U Server started on port {self.port}")
            return True
        except Exception as e:
            logging.error(f"Failed to start M3U Server: {e}")
            self.server = None
            return False

    def stop(self):
        """Stop the server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
            self.thread = None
            logging.info("M3U Server stopped")

    def is_running(self):
        """Check if server is running."""
        return self.server is not None
