from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 5001
counter = 0

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        global counter

        if self.path == "/":
            html = f"""
            <html>
            <body>
                <h1>Counter (in memory)</h1>
                <button onclick="fetch('/count').then(r => r.text()).then(t => document.getElementById('result').innerText = t)">
                    Klick mich
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
            counter += 1
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Counter: {counter}".encode())

with HTTPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Server running on port {PORT}")
    httpd.serve_forever()
