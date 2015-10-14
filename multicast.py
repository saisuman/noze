import struct
import config
import log
import socket
import threading
import time

"""Handles multicasting of discovery messages."""
class Multicaster(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._terminated = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        log.i('Started up multicast thread, advertising %s:%d, multicast group %s:%d',
              config.SERVER_BIND_ADDRESS, config.SERVER_BIND_PORT,
              config.DISCOVERY_MULTICAST_GROUP, config.DISCOVERY_MULTICAST_PORT)

    def terminate():
        _terminated = True

    def make_noze_server_url(self):
        return 'http://%s:%d' % (
            config.SERVER_BIND_ADDRESS, config.SERVER_BIND_PORT)

    def run(self):
        i = 0
        while not self._terminated:
            message = "noze_server|%s|%d" % (
                config.SERVER_BIND_ADDRESS,
                config.SERVER_BIND_PORT)

            self.sock.sendto(message,
                             (config.DISCOVERY_MULTICAST_GROUP,
                              config.DISCOVERY_MULTICAST_PORT))
            i += 1
            if i % 100 == 0:
                i = 0
                log.d('Multicasted %s on group %s:%d',
                      message, config.DISCOVERY_MULTICAST_GROUP,
                      config.DISCOVERY_MULTICAST_PORT)
            time.sleep(5)

"""Returns a discovery message by joining the right multicast group."""
def discover_server_url():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', config.DISCOVERY_MULTICAST_PORT))
    mreq = struct.pack("=4sl", socket.inet_aton(config.DISCOVERY_MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    message = None
    while True:
        try:
            message = sock.recv(1024, socket.MSG_DONTWAIT)
            print message
            break
        except socket.error as e:
            if e.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
                continue
            log.e('Some socket error in discover server.')
            return
    print message
    parts = message.split('|')
    if len(parts) != 2 or parts[0] != 'noze_server':
        raise RuntimeError('Someone is messing with the multicast group: %s' % message)
    return parts[1]


              
