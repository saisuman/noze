import sqlite3

import backend

STATE_ACTIVE = 'active'  # Pinged recently.
STATE_STALE = 'inactive'  # Pinged a long time ago.
STATE_DEAD = 'dead'  # Pinged a very, very long time ago.

def get_active_nodes():
    c = backend.db().cursor()
    states = [STATE_ACTIVE]
    c.execute('SELECT name, addr, last_heartbeat_ts, state FROM nodestate WHERE state = ?', states)
    return c.fetchall()

def update_node(name, addr, last_heartbeat_ts, state):
    c = backend.db().cursor()
    c.execute('UPDATE nodestate SET addr=?, last_heartbeat_ts=?, state=? WHERE name=?',
              (addr, last_heartbeat_ts, state, name))
    c.execute('INSERT OR IGNORE INTO nodestate VALUES(?, ?, ?, ?)',
              (name, addr, last_heartbeat_ts, state))
    backend.db().commit()
    return True
