from BaseHTTPServer import BaseHTTPRequestHandler
import flags
import protocol
import urlparse
import net_util
import log
import gflags
import base64

FLAGS = gflags.FLAGS

PARAM_PAYLOAD = 'payload'

def handler_class_with_action(server_instance):
    class GetHandler(BaseHTTPRequestHandler):
        def __init__(self, *args):
            BaseHTTPRequestHandler.__init__(self, *args)

        def do_GET(self):
            parsed_path = urlparse.urlparse(self.path)
            endpoint = parsed_path.path
            querystring_params = urlparse.parse_qs(parsed_path.query)
            payloads = querystring_params.get(PARAM_PAYLOAD, [])
            if not payloads:
                payload = None
            else:
                payload = base64.b64decode(payloads[0])
            try:
                request = protocol.Request(json_text=payload, endpoint=endpoint)
                try:
                    response = server_instance.execute(request)
                    code = response.code
                except Exception as e:
                    log.ex('Could not provide response.')
                    response = protocol.RESPONSE_INTERNAL_ERROR
                    code = 500
            except Exception as e:
                log.ex('Could not process request.')
                response = protocol.RESPONSE_INVALID_REQUEST
                code = 400
            self.send_response(code)
            self.send_header("Content-type", "text/json")
            self.end_headers()
            self.wfile.write(response.to_json())

        #def log_message(unused_arg1, unused_arg2, *args):
        #    pass  # noisy
    return GetHandler

def new_server(server_instance):
    from BaseHTTPServer import HTTPServer
    log.i('Starting a server on all interfaces.')
    server = HTTPServer(('', FLAGS.server_bind_port), 
                        handler_class_with_action(server_instance))
    return server
