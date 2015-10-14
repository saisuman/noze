#!/usr/bin/python
import protocol
import multicast
import StringIO
import webserver
import node_action
import log
import threading
import config
import pycurl

class Pinger(threading.Thread):
    def __init__(self, sever_url):
        threading.Thread.__init__(self)
        self.server_url = server_url
        self._terminated = False

    def terminate(self):
        self._terminated = True

    def make_ping_url(self):
        return '%s/ping?payload=%s' %(
            self.server_url,
            json.puts({
                'name': 'raspberry',
                'addr': '192.168.0.26',
                'state': 'ALIVE'
            }))

    def run(self):
        while not _terminated:
            c = pycurl.Curl()
            c.setopt(c.URL, self.make_ping_url())
            empty_buf = StringIO()
            c.perform()
            c.close()
            sleep(5)


if __name__ == '__main__':
    server = webserver.new_server(node_action)
    server = multicast.discover_server()
    

    # Now start the node
    log.i('Starting node, use <Ctrl-C> to stop')
    server.serve_forever()
    multicast_thread.terminate()
