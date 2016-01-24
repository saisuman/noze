import struct
import errno
import flags
import log
import socket
import threading
import time
import gflags
import net_util

FLAGS = gflags.FLAGS


"""Handles multicasting of discovery messages."""
class Multicaster(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._terminated = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        log.i('Started up multicast thread, advertising %s:%d, multicast group %s:%d',
              net_util.get_server_ip(), FLAGS.server_bind_port,
              net_util.get_server_ip(), FLAGS.discovery_multicast_port)

    def terminate():
        _terminated = True

    def make_noze_server_url(self):
        return 'http://%s:%d' % (
            net_util.get_server_ip(), FLAGS.server_bind_port)

    def run(self):
        i = 0
        message = 'noze_root|%s' % self.make_noze_server_url()
        while not self._terminated:
            self.sock.sendto(message,
                             (FLAGS.discovery_multicast_group,
                              FLAGS.discovery_multicast_port))
            i += 1
            if i % 100 == 0:
                i = 0
                log.d('Multicasted %s on group %s:%d',
                      message, FLAGS.discovery_multicast_group,
                      FLAGS.discovery_multicast_port)
            time.sleep(5)

"""Returns a discovery message by joining the right multicast group."""
def discover_root_node_url():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', FLAGS.discovery_multicast_port))
    mreq = struct.pack("=4sl", socket.inet_aton(FLAGS.discovery_multicast_group), socket.INADDR_ANY)
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
            log.e('Some socket error in discover root.')
            return
    print message
    parts = message.split('|')
    if len(parts) != 2 or parts[0] != 'noze_root':
        raise RuntimeError('Someone is messing with the multicast group: %s' % message)
    return parts[1]
