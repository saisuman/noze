var flags = require('./flags');

var express = require('express');
var app = express();

// index.html is mapped to / by default.
app.use('/static', express.static('static'));

var rpc = require('./rpc');
var root = require('./root');

app.get('/action_update', function(req, res) {
    console.log('Responding to action update.');
    root.updateNode(rpc.getActionPayload(req), function(status, payload) {
	rpc.sendResponse(status, payload, res);
    });
});

app.get('/action_query', function(req, res) {
    console.log('Responding to action query.');
    root.getNodes(rpc.getActionPayload(req), function(status, payload) {
	console.log('getNodes yielded:', payload, status);
	rpc.sendResponse(status, payload, res);
    });
});

app.listen(flags.port, function() {
    console.log('Started server on port:' + flags.port);
});
