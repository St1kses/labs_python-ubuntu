from http.server import HTTPServer, BaseHTTPRequestHandler
class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = b"<!DOCTYPE html><html><head><meta charset=utf-8><title>Hello</title></head>"
            body += b"<body><h1>Hello, World!</h1></body></html>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)
    def log_message(self, format, *args):
        pass
if __name__ == "__main__":
    host, port = "0.0.0.0", 5000
    print(f"Сервер: http://{host}:{port}/ (откройте в браузере IP машины)")
    HTTPServer((host, port), HelloHandler).serve_forever()
