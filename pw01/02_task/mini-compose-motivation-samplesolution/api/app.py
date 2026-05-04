from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random

PORT = 5001

QUOTES = [
    "Keep going.",
    "Small steps matter.",
    "Progress beats perfection.",
    "You learn by doing.",
    "Every error teaches something."
]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/quote":
            message = random.choice(QUOTES)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"quote": message}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")

with HTTPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"API running on port {PORT}")
    httpd.serve_forever()
