var flags = require('./flags');
var discovery = require('./discovery');
var express = require('express');
var app = express();

app.use('/static', express.static('static'));
app.get('/', function(req, res) { res.redirect(301, '/static/index.html'); });

var rpc = require('./rpc');

module.exports = {
    // Starts pinging.
    startPinger: function() {
	pinger.start();
    },

    subscribe: function(subscribeSpec) {
	
    },

    publish: function(publishMessage) {

    }
};
