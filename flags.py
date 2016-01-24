import gflags

gflags.DEFINE_integer('server_bind_port', 8080, 'The server port to bind to.')
gflags.DEFINE_string('server_bind_address', '', 'The server address to bind to.')
gflags.DEFINE_integer('discovery_multicast_port', 51525, 'The multicast port for discovery.')
gflags.DEFINE_string('discovery_multicast_group', '224.51.52.53', 'The multicast group for discovery.')
