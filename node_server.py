import base64
import time
import base_server
import sys
import socket
import json
import gflags
import protocol
import multicast
import StringIO
import net_util
import webserver
import log
import threading
import flags
import pycurl

FLAGS = gflags.FLAGS

class Pinger(threading.Thread):
    def __init__(self, root_node_url):
        threading.Thread.__init__(self)
        self.root_node_url = root_node_url
        self._terminated = False

    def terminate(self):
        self._terminated = True

    def make_ping_url(self):
        return '%s/ping?payload=%s' %(
            self.root_node_url,
            base64.b64encode(json.dumps({
                'name': socket.gethostname(),
                'addr':  net_util.get_server_ip(),
                'state': 'ALIVE'
            })))

    def run(self):
        while not self._terminated:
            c = pycurl.Curl()
            c.setopt(c.URL, self.make_ping_url())
            empty_buf = StringIO.StringIO()
            c.setopt(c.WRITEDATA, empty_buf)
            c.perform()
            c.close()
            time.sleep(5)


if __name__ == '__main__':
    argv = FLAGS(sys.argv)
    webserver = webserver.new_server(base_server.BaseServer())
    root_node_url = multicast.discover_root_node_url()
    p = Pinger(root_node_url=root_node_url)
    p.start()
    
    # Now start the node
    log.i('Starting node, use <Ctrl-C> to stop')
    webserver.serve_forever()
    multicast_thread.terminate()
