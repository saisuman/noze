import webserver
import gflags
import multicast
import protocol
import base_server
import db
import json
import log
import os
import sys
import signal

from obj import node

ENDPOINT_PING = '/ping'
ENDPOINT_QUERY_ACTIVE = '/query_active'

class RootServer(base_server.BaseServer):
    def register_handlers(self):
        base_server.BaseServer.register_handlers(self)
        self.register(ENDPOINT_PING, self._ping_handler)
        self.register(ENDPOINT_QUERY_ACTIVE, self._query_active_handler)

    def _query_active_handler(self, endpoint, request):
        rows = db.get_active_nodes()
        active_nodes = [node.Node(row=r).to_dict() for r in rows]
        log.d('Returning %d active nodes from query.', len(active_nodes))
        return protocol.Response(status=protocol.STATUS_OK, payload=active_nodes)

    def _ping_handler(self, endpoint, request):
        n = node.Node(json_dict=request.payload)
        log.d('Updating Node object: %s', node)
        db.update_node(n.name, n.addr, n.last_heartbeat_ts, n.state)    
        return protocol.RESPONSE_OK


if __name__ == '__main__':
    argv = gflags.FLAGS(sys.argv)
    server = webserver.new_server(RootServer())
    # Start up the multicaster that advertises the location of the root
    # node on a multicast group.
    multicast_thread = multicast.Multicaster()
    multicast_thread.start()

    # Now start the server
    log.i('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
    multicast_thread.terminate()
