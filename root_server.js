var flags = require('./flags');
var broadcaster = require('./broadcaster');

var express = require('express');
var app = express();
var server = require('http').createServer(app);

server.listen(flags.port, function() {
    console.log('Started server on port:' + flags.port);
});


app.use('/static', express.static('static'));
app.get('/', function(req, res) { res.redirect(301, '/static/index.html'); });

var rpc = require('./rpc');
var root = require('./root');

broadcaster.start();

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



