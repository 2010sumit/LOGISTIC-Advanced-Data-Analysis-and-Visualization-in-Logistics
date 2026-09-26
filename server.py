"""
Local HTTP Web Server for Logistics Dashboard
Author: SUMIT KUMAR (SUMIT277203YT@GMAIL.COM | 9120329201)
"""

import http.server
import socketserver
import os
import sys

PORT = 8000

class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress verbose log noise in terminal
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

def run_server():
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)
    
    handler = QuietHTTPRequestHandler
    
    # Allow port reuse to avoid 'Address already in use' errors
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"==================================================================")
        print(f" LOGISTICS DASHBOARD LOCALHOST SERVER IS LIVE!")
        print(f" Lead Analyst: SUMIT KUMAR | SUMIT277203YT@GMAIL.COM | 9120329201")
        print(f" Access Link: http://localhost:{PORT}")
        print(f" Access Link: http://127.0.0.1:{PORT}")
        print(f"==================================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Server shutting down.")
            httpd.server_close()

if __name__ == "__main__":
    run_server()
