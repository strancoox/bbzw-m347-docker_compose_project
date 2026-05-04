from http.server import BaseHTTPRequestHandler, HTTPServer
import os

PORT = 5001
DATA_DIR = "/data"
FILE = os.path.join(DATA_DIR, "counter.txt")


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def read_counter():
    ensure_data_dir()
    if not os.path.exists(FILE):
        return 0
    with open(FILE, "r") as f:
        content = f.read().strip()
        return int(content) if content else 0


def write_counter(value):
    ensure_data_dir()
    with open(FILE, "w") as f:
        f.write(str(value))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            counter = read_counter()
            html = f"""
            <html>
            <body>
                <h1>Counter (file + volume)</h1>
                <button onclick="fetch('/count').then(r => r.text()).then(t => document.getElementById('result').innerText = t)">
                    Click me
                </button>
                <p id="result">Counter: {counter}</p>
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        elif self.path == "/count":
            counter = read_counter() + 1
            write_counter(counter)
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Counter: {counter}".encode())

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")


with HTTPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Server running on port {PORT}")
    print(f"Counter file: {FILE}")
    httpd.serve_forever()