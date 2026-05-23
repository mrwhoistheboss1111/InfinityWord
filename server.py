from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen


class QBankHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/proxy":
            self.proxy_request(parsed)
            return
        super().do_GET()

    def proxy_request(self, parsed):
        target = parse_qs(parsed.query).get("url", [""])[0]
        if not target.startswith(("https://diuqbank.com/", "https://diuqbank-com.sgp1.cdn.digitaloceanspaces.com/")):
            self.send_error(400, "Unsupported proxy target")
            return

        try:
            req = Request(
                target,
                headers={
                    "User-Agent": "Mozilla/5.0 DIU-QBank-local-viewer",
                    "Referer": "https://diuqbank.com/",
                },
            )
            with urlopen(req, timeout=25) as upstream:
                data = upstream.read()
                content_type = upstream.headers.get("Content-Type", "application/octet-stream")
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
        except Exception as exc:
            self.send_error(502, f"Proxy fetch failed: {exc}")


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8787), QBankHandler)
    print("DIU QBank running at http://127.0.0.1:8787/index.html")
    server.serve_forever()
