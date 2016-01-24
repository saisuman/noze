#!/bin/bash

server_port="8081"
node_ports="8091"

if [ "$1" == "start" ]; then
	echo "Starting a server."
	setsid python root_server.py --server_bind_port=$server_port &
	echo "Starting nodes..."
	for i in $node_ports; do
		setsid python node_server.py --server_bind_port=$i &
	done;
	echo "Started everything."
elif [ "$1" == "stop" ]; then
	echo "Killing everything..."
	for i in $server_port $node_ports; do
		curl http://localhost:$i/die
	done;
fi;
