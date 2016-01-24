import log

class Node(object):
    def __init__(self, row=None, json_dict=None):
        if row is not None:
            self.name, self.addr, self.last_heartbeat_ts, self.state = row
        elif json_dict is not None:
            self.name = json_dict.get('name', '')
            self.addr = json_dict.get('addr', '')
            self.last_heartbeat_ts = json_dict.get('last_heartbeat_ts', '')
            self.state = json_dict.get('state', '')
            if not self.name and not self.addr and not self.state:
                raise AttributeError('Badly formed Node object: %s' % json_dict)
        else:
            raise RuntimeError('Either row or json should be specified.')
        log.d('Initialised Node object: %s', self)

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return '(name=%s, addr=%s, last_heartbeat_ts=%s, state=%s)' % (
            self.name, self.addr, self.last_heartbeat_ts, self.state)

    def __str__(self):
        return self.__repr__()
