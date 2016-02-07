#!/usr/bin/env python

import sys
import os
import mimetypes
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from langmodel.generate import generate_text

port_number = sys.argv[1] if len(sys.argv) > 1 else 9999

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(SCRIPT_DIR, "..", "build", "text_template")
STATIC_ROOT = os.path.join(SCRIPT_DIR, "static")


class LorumIpseHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        if path == "/":
            path = "/static/index.html"
        if path.startswith('/static/') and '..' not in path:
            self.serve_static_file(path[len("/static/"):])
        elif path.startswith('/generate/'):
            init = "/generate/init/" in path
            text = generate_text(TEMPLATE_DIR, init)
            self.send_response(200)
            self.send_header("Content-type", "text/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(text.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def serve_static_file(self, path):
        abs_path = os.path.join(STATIC_ROOT, path)
        if os.path.isfile(abs_path):
            with open(abs_path, "r") as f:
                content = f.read()
            mime_type, encoding = mimetypes.guess_type(abs_path)
            if mime_type.startswith("text/"):
                content_type = mime_type + "; charset=utf-8"
            else:
                content_type = mime_type
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()
        

mimetypes.init()
server = HTTPServer(('', port_number), LorumIpseHandler)
server.serve_forever()

