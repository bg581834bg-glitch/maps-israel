# static_server.py
import http.server
import socketserver
import os
import webbrowser

PORT = 8000
SERVE_DIR = r'c:\maps\tiles'

os.chdir(SERVE_DIR)  # מעבר לתיקיית ההגשה

Handler = http.server.SimpleHTTPRequestHandler

def open_browser():
    webbrowser.open(f'http://localhost:{PORT}/')

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        open_browser()
        httpd.serve_forever()
