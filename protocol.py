import json
import base64
import log

TAG_STATUS = 'status'
TAG_STATUS_TEXT = 'status_text'
TAG_PAYLOAD = 'payload'

STATUS_OK = 1
STATUS_UNKNOWN = 2
STATUS_UNINITIALIZED = 0
STATUS_INVALID_REQUEST = 3
STATUS_INTERNAL_ERROR = 4

ERR_DICT = {
    STATUS_OK: "OK",
    STATUS_UNINITIALIZED: "Uninitialised state. Possibly a bug.",
    STATUS_INTERNAL_ERROR: "Internal server error.",
    STATUS_INVALID_REQUEST: "Bad / invalid request from client.",
    STATUS_UNKNOWN: "Unforeseen error condition."
}


class Response(object):
    def __init__(self, status=None, code=200, payload=None):
        self.status = RESPONSE_OK if status is None else status
        self.payload = payload
        self.code = code
        self.status_text = ERR_DICT[status]

    def status(self):
        return self.status

    def to_json(self):
        return json.dumps({
            TAG_STATUS: self.status,
            TAG_STATUS_TEXT: self.status_text,
            TAG_PAYLOAD: self.payload})

class Request(object):
    def __init__(self, json_text=None, endpoint=None):
        if json_text:
            try:
                self.payload = json.loads(json_text)
            except ValueError as e:
                log.ex('Parse error in json parsing %s.', json_text)
                raise
        else:
            self.payload = {}
        self.status = self.payload.get(TAG_STATUS, STATUS_UNINITIALIZED)
        self.endpoint = endpoint

    def __str__(self):
        return 'ENDPOINT: %s, status=%s, payload=%s' % (self.endpoint, self.status, self.payload)

RESPONSE_OK = Response(STATUS_OK, code=200)
RESPONSE_INVALID_REQUEST = Response(STATUS_INVALID_REQUEST, code=400)
RESPONSE_INTERNAL_ERROR = Response(STATUS_INTERNAL_ERROR, code=500)
