import protocol
import json
import log
import config


ENDPOINT_DO = '/do'

def execute(request):
    log.d('Processing request: %s', request)
    if request.endpoint == ENDPOINT_DO:
        return action(DO)
    return protocol.RESPONSE_INVALID_REQUEST

def do(request):
    return protocol.Response(status=protocol.STATUS_OK)

