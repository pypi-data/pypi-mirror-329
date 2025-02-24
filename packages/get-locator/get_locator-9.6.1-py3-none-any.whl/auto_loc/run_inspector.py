# auto_loc/run_inspector.py

import argparse
import json
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from auto_loc import WebInspector

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/reload_url':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            url = data.get('url')
            self.server.inspector.driver.get(url)  # Загружаем новый URL
            self.server.inspector.current_url = url  # Обновляем контекст
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"URL reloaded successfully")

    def log_message(self, format, *args):
        return  # Отключение стандартного вывода логов HTTP-сервера

def main():
    parser = argparse.ArgumentParser(description="Run Web Inspector")
    parser.add_argument('--url', type=str, help="URL to start the Web Inspector")
    parser.add_argument('--attributes', type=str, nargs='*', default=["data-test-id", "data-e2e", "test-id"],
                        help="List of test attributes for locator generation")
    args = parser.parse_args()

    url = args.url or "https://example.com"
    test_attributes = args.attributes

    inspector = WebInspector(test_attributes=test_attributes)
    inspector.start(url)

    server = HTTPServer(('localhost', 8000), RequestHandler)
    server.inspector = inspector

    print(f"Starting server at http://localhost:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
    finally:
        inspector.quit()
        server.server_close()

if __name__ == "__main__":
    main()