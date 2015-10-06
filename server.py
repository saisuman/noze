#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
import protocol
import json
import action
import log

TAG_PAYLOAD = 'payload'

class GetHandler(BaseHTTPRequestHandler):    
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        endpoint = parsed_path.path
        querystring_params = urlparse.parse_qs(parsed_path.query)
        payloads = querystring_params.get(TAG_PAYLOAD, [])
        if not payloads:
            payload = None
        else:
            payload = payloads[0]
        try:
            request = protocol.Request(payload, endpoint)
            try:
                response = action.execute(request)
                code = 200
            except Exception as e:
                log.ex('Could not provide response.')
                response = protocol.RESPONSE_INTERNAL_ERROR
                code = 500
        except Exception as e:
            log.ex('Could not process request.')
            response = protocol.RESPONSE_INVALID_REQUEST
            code = 400
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response.to_json())

    def log_message(unused_arg1, unused_arg2, *args):
        pass  # noisy

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('', 8080), GetHandler)
    log.i('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
