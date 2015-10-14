#!/usr/bin/python
import protocol
import multicast
import webserver
import server_action
import log
import config


if __name__ == '__main__':
    server = webserver.new_server(server_action)
    # Start up the multicaster that advertises the location of the server
    # on a multicast group.
    multicast_thread = multicast.Multicaster()
    multicast_thread.start()

    # Now start the server
    log.i('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
    multicast_thread.terminate()
