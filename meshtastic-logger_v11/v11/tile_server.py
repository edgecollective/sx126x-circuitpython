#!/usr/bin/env python3
"""
Simple HTTP server to serve map tiles locally
"""

import os
import http.server
import socketserver
from urllib.parse import urlparse, unquote

class TileHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=".", **kwargs)
    
    def do_GET(self):
        """Handle GET requests for tiles and other files"""
        parsed_path = urlparse(self.path)
        path = unquote(parsed_path.path)
        
        # Handle tile requests
        if path.startswith('/tiles/'):
            # Remove leading slash and serve from tiles directory
            file_path = path[1:]  # Remove leading slash
            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'max-age=86400')  # Cache for 1 day
                self.end_headers()
                
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_error(404, f"Tile not found: {file_path}")
                return
        
        # Handle static files (Leaflet CSS, JS, images)
        if path.startswith('/static/'):
            file_path = path[1:]  # Remove leading slash
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # Determine content type
                if file_path.endswith('.css'):
                    content_type = 'text/css'
                elif file_path.endswith('.js'):
                    content_type = 'application/javascript'
                elif file_path.endswith('.png'):
                    content_type = 'image/png'
                else:
                    content_type = 'application/octet-stream'
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'max-age=86400')  # Cache for 1 day
                self.end_headers()
                
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_error(404, f"Static file not found: {file_path}")
                return
        
        # Handle other files (HTML, CSS, JS, CSV, etc.)
        if path == '/':
            path = '/index.html'
        
        file_path = path[1:]  # Remove leading slash
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # Determine content type
            if file_path.endswith('.html'):
                content_type = 'text/html'
            elif file_path.endswith('.css'):
                content_type = 'text/css'
            elif file_path.endswith('.js'):
                content_type = 'application/javascript'
            elif file_path.endswith('.csv'):
                content_type = 'text/csv'
            elif file_path.endswith('.json'):
                content_type = 'application/json'
            else:
                content_type = 'text/plain'
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, f"File not found: {file_path}")
    
    def log_message(self, format, *args):
        """Override to provide cleaner logging"""
        message = format % args
        print(f"[{self.address_string()}] {message}")

def main():
    PORT = 8090
    
    print(f"Starting tile server on port {PORT}")
    print(f"Serving from: {os.getcwd()}")
    print(f"Access the map at: http://localhost:{PORT}/")
    print("Press Ctrl+C to stop")
    
    with socketserver.TCPServer(("", PORT), TileHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == "__main__":
    main()
