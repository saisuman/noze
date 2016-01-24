import protocol
import db
import json
import log
import os
import signal

ENDPOINT_PING = '/ping'
ENDPOINT_QUERY_ACTIVE = '/query_active'
ENDPOINT_DIE = '/die'

def execute(request):
    log.d('Processing request: %s', request)
    if request.endpoint == ENDPOINT_QUERY_ACTIVE:
        return query_active(request)
    elif request.endpoint == ENDPOINT_PING:
        return update_node(request)
    elif request.endpoint == ENDPOINT_DIE:
        log.i('Told to kill self. Complying.')
        os.kill(os.getpid(), signal.SIGTERM)        
    return protocol.RESPONSE_INVALID_REQUEST

class Node(object):
    def __init__(self, row=None, json_dict=None):
        if row is not None:
            self.name, self.addr, self.last_heartbeat_ts, self.state = row
        elif json_dict is not None:
            self.name = json_dict.get('name', '')
            self.addr = json_dict.get('addr', '')
            self.last_heartbeat_ts = json_dict.get('last_heartbeat_ts', '')
            self.state = json_dict.get('state', '')
        log.d('Initialised Node object: %s', self)

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return '(name=%s, addr=%s, last_heartbeat_ts=%s, state=%s)' % (
            self.name, self.addr, self.last_heartbeat_ts, self.state)

    def __str__(self):
        return self.__repr__()

def query_active(request):
    rows = db.get_active_nodes()
    active_nodes = [Node(row=r).to_dict() for r in rows]
    log.d('Returning %d active nodes from query.', len(active_nodes))
    return protocol.Response(status=protocol.STATUS_OK, payload=active_nodes)

def update_node(request):
    node = Node(json_dict=request.payload)
    log.d('Updating Node object: %s', node)
    db.update_node(node.name, node.addr, node.last_heartbeat_ts, node.state)
    return protocol.RESPONSE_O
