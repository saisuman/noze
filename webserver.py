from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
import log

PARAM_PAYLOAD = 'payload'


def handler_class_with_action(action_module):
    class GetHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed_path = urlparse.urlparse(self.path)
            endpoint = parsed_path.path
            querystring_params = urlparse.parse_qs(parsed_path.query)
            payloads = querystring_params.get(PARAM_PAYLOAD, [])
            if not payloads:
                payload = None
            else:
                payload = payloads[0]
                try:
                    request = protocol.Request(payload, endpoint)
                    try:
                        response = action_module.execute(request)
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


def new_server(action_module):
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('', config.SERVER_BIND_PORT), handler_class_with_action(action_module))
    return server

