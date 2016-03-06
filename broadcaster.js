var flags = require('./flags');
var ip = require('ip');
const dgram = require('dgram');

createBroadcastMessage = function() {
    return "http://" + ip.address().toString() + ":" + flags.port;
};

startBroadcasting = function() {
    const message = new Buffer(createBroadcastMessage());
    var client = dgram.createSocket('udp4');
    client.bind(function (err) {
	if (err) {
	    console.log('ERROR: could not bind broadcast port!!');
	    return;
	}
	client.setBroadcast(true);
	sendIt(client, message);
    });
};

sendIt = function(client, message) {
    console.log('Sending bytes:' + message.length);
    client.send(message, 0, message.length, flags.broadcastPort, "255.255.255.255", function(err) {
	if (err) {
	    console.log('ERROR sending broadcast!: ' + err);
	    return;
	}
	console.log('Sent broadcast message: ' + message.toString());
    });
    setTimeout(function() { sendIt(client, message); }, 10000);
};

module.exports = {
    start: startBroadcasting
};
