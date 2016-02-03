#!/bin/bash

SQLITE3=/usr/bin/sqlite3

query="CREATE TABLE nodestate ( \
  name text, \
  addr text, \
  last_heartbeat_ts integer, \
  state text, \
  PRIMARY KEY(name ASC));"

echo $query | $SQLITE3 --batch noze.db
if [ $? != 0 ]; then
    echo "FAILED!"
fi;
