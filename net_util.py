import flags
import gflags

FLAGS = gflags.FLAGS

def get_server_ip():
    if FLAGS.server_bind_address:
        return FLAGS.server_bind_address
    import netifaces
    for interface in netifaces.interfaces():
        if interface == 'lo':
            continue
        addresses = netifaces.ifaddresses(interface)
        ip = addresses.get(netifaces.AF_INET, None)
        if ip:
            return ip[0]['addr']
    return FLAGS.server_bind_address
