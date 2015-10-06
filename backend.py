import sqlite3

_conn = sqlite3.connect('noze.db')

def db():
    return _conn
