import gflags

FLAGS = gflags.FLAGS

gflags.DEFINE_integer('server_bind_port', 8080, 'The server port to bind to.')
gflags.DEFINE_string('server_bind_address', '192.168.0.22', 'The server address to bind to.')
gflags.DEFINE_integer('multicast_port', 51525, 'The multicast port for discovery.')
gflags.DEFINE_string('multicast_group', '224.51.52.53', 'The multicast group for discovery.')

# The discovery multicast group and port for the nodes to discover
# where the server lives.
DISCOVERY_MULTICAST_GROUP = FLAGS.multicast_group
DISCOVERY_MULTICAST_PORT = FLAGS.multicast_port

SERVER_BIND_ADDRESS = FLAGS.server_bind_address
SERVER_BIND_PORT = FLAGS.server_bind_port
