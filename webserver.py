# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from routes import *


class RequestHandler(BaseHTTPRequestHandler):
    """Handle HTTP requests by returning a fixed 'page'."""

    cases = [CaseNoFile(),
             CaseCGIFile(),
             CaseExistingFile(),
             CaseDirectoryIndexFile(),
             CaseDirectoryNoIndexFile(),
             CaseAlwaysFail()]

    ERROR_PAGE = '''\
    <html>
    <body>
    <h1>Error accessing {path}</h1>
    <p>{msg}</p>
    </body>
    </html>
    '''

    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path
            for case in self.cases:
                if case.test(self):
                    case.act(self)
                    break

        except Exception as msg:
            self.handle_error(msg)

    def handle_error(self, msg):
        content = self.ERROR_PAGE.format(path=self.path, msg=msg)
        self.send_content(content, 404)

    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        if not isinstance(content, bytes):
            content = bytes(content, 'utf8')
        self.wfile.write(content)


if __name__ == '__main__':
    server_address = ('', 8080)
    server = HTTPServer(server_address, RequestHandler)
    server.serve_forever()