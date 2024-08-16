from http.server import BaseHTTPRequestHandler
import cgi


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # self.send_response(200)
        # self.end_headers()
        # self.wfile.write(b'Hello World!')
        pass

    def do_POST(self):
        pass

    def do_PUT(self):
        pass