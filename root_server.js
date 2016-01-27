var flags = require('./flags');

var express = require('express');
var app = express();

// index.html is mapped to / by default.
app.use(express.static('static'));

var rpc = require('./rpc');
var root = require('./root');

app.get('/action_update', function(req, res) {
    rpc.sendResponse(
	root.updateNode(rpc.getActionPayload(req)),
	res);
});

app.listen(flags.port, function() {
    console.log('Started server on port:' + flags.port);
});
