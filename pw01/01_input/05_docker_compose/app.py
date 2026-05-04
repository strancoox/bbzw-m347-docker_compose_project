from http.server import BaseHTTPRequestHandler, HTTPServer
import redis

PORT = 5001
r = redis.Redis(host="redis", port=6379)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            html = """
            <html>
            <body>
                <h1>Counter (Docker Compose)</h1>
                <button onclick="fetch('/count').then(r => r.text()).then(t => document.getElementById('result').innerText = t)">
                    Click me
                </button>
                <p id="result">No clicks yet</p>
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        elif self.path == "/count":
            count = r.incr("counter")
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Counter: {count}".encode())

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")


with HTTPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Server running on port {PORT}")
    print("Redis host: redis")
    httpd.serve_forever()