import protocol
import db
import json
import log
import os
import signal

ENDPOINT_DIE = '/die'
ENDPOINT_STATUS = '/'

class BaseServer(object):
    def __init__(self):
        self._handlers = {}
        self.register_handlers()

    def register_handlers(self):
        self.register(ENDPOINT_DIE, self._die_handler)
        self.register(ENDPOINT_STATUS, self._status_handler)

    def register(self, endpoint, method):
        if endpoint in self._handlers:
            raise RuntimeError('%s is already registered.' % endpoint)
        self._handlers[endpoint] = method

    def execute(self, request):
        log.d('Processing request: %s', request)
        handler = self._handlers.get(request.endpoint, None)
        if handler is None:
            return protocol.RESPONSE_INVALID_REQUEST
        return handler(request.endpoint, request)

    def _die_handler(self, endpoint, request):
        log.i('Told to kill self. Complying.')
        os.kill(os.getpid(), signal.SIGTERM)
        return protocol.RESPONSE_OK

    def _status_handler(self, endpoint, request):
        log.i('Serving status response.')
        return protocol.RESPONSE_OK
