var flags = require('./flags');
var ip = require('ip');
const dgram = require('dgram');

createBroadcastMessage = function() {
    return "http://" + ip.address().toString() + ":" + flags.port;
};

startBroadcasting = function(port) {
    const message = new Buffer(createBroadcastMessage());
    const client = dgram.createSocket('udp4');
    sendIt(client, message);
};

sendIt = function(client, message) {
    client.send(message, 0,  message.length, flags.broadcastPort, "255.255.255.255", function(err) {
	console.log('Sent broadcast message: ' + message.toString());
    });
    setTimeout(function() { sendIt(client, message); }, 10000);
};

module.exports = {
    start: startBroadcasting
};
