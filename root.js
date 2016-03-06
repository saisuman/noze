var rpc = require('./rpc');
var flags = require('./flags');
var sqlite3 = require('sqlite3').verbose();
var database = new sqlite3.Database(flags.databaseFile);

var NODE_STATUSES = {
    STATE_ACTIVE: 'ACTIVE',
    STATE_ERROR: 'ERROR',
    STATE_STALE: 'STALE',
    STATE_UNKNOWN: 'UNKNOWN'
};

var STALE_TIMEOUT_S = 10 * 60 * 1000;  // 10 minutes.

Node = function(name, addr, state, last_heartbeat_ts) {
    this.name = name;
    this.addr = addr;
    this.state = state;
    this.last_heartbeat_ts = last_heartbeat_ts;
};

function nodeFromRow(row) {
    return new Node(row.name, row.addr, row.state, row.last_heartbeat_ts);
}

isValidNodeStatus = function(payload) {
    if (!payload) {
	return false;
    }
    if (payload.name && payload.name.trim() &&
	payload.addr && payload.addr.trim() &&
	payload.state && payload.state.trim()) {
	return true;
    }
    return false;
};

module.exports = {
    broadcastMessage: function(payload, callback) {
	console.log('Broadcast request with payload: ' + JSON.stringify(payload));
	
    },

    updateNode: function(payload, callback) {
	console.log('Update request with payload: ' + JSON.stringify(payload));
	if (!isValidNodeStatus(payload)) {
	    callback(rpc.STATUS_REQUEST_ERROR, {});
	    return;
	}
	var node = payload;
	var stmt = database.prepare(
	    'INSERT OR REPLACE INTO nodestate(name, addr, last_heartbeat_ts, state) ' +
		'VALUES(COALESCE((SELECT name from nodestate where name = ?), ?), ?, ?, ?)',
	    node.name, node.name, node.addr, Date.now(), node.state);
	console.log('Updating node state for ' + node.name + ' from ' + node.addr);
	stmt.run(function() { callback(rpc.RESPONSE_OK); });
    },

    getNodes: function(payload, callback) {
	database.all('SELECT name, addr, last_heartbeat_ts, state FROM nodestate;',
		     function(err, rows) {
			 var nodes = new Array();
			 rows.forEach(function(row) {
			     nodes.push(nodeFromRow(row));
			 });
			 callback(rpc.STATUS_OK, nodes);
		     });
    },
    
    startNodeStateUpdater: function() {
	markNodesAsStale = function() {
	    var stmt = database.prepare(
		'UPDATE nodestate SET state=? WHERE last_heartbeat_ts < ?',
		NODE_STATUSES.STATE_STALE, Date.now() - STALE_TIMEOUT_S);
	    stmt.run(function() {
		console.log('Ran updater.');
		setTimeout(markNodesAsStale, 10000);
	    });
	};
	markNodesAsStale();
    }
};

// Runs the reaper that updates the known states of old nodes.
module.exports.startNodeStateUpdater();
