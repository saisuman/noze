var dgram = require('dgram');
var flags = require('./flags');
var express = require('express');
var app = express();

app.use('/static', express.static('static'));
app.get('/', function(req, res) { res.redirect(301, '/static/index.html'); });

var rpc = require('./rpc');

module.exports = {
    start: function() {
	var server = dgram.createSocket('udp4');
	server.on('message', function(msg, rinfo) {
	    console.log('Discovery message payload: ' + msg);
	    server.close();  // Other processes on the same host may need it.
	});

	server.on('error', function(err) {
	    console.log('server error: ', err);
	    server.close();
	});
	
	server.on('listening', function(err) {
	    var address = server.address();
	    console.log('server listening ', address.address, address.port);
	    server.setBroadcast(true);
	});

	server.bind(flags.broadcastPort, function(err) {
	    server.setBroadcast(true);
	    if (err) {
		console.log(err.stack);
		return;
	    }
	    console.log('Bound.');
	    
	});
    }
};

module.exports.start();
