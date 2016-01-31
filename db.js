var flags = require('./flags');
var sqlite3 = require('sqlite3').verbose();
var database = new sqlite3.Database(flags.databaseFile);

Node = function(name, addr, state, last_heartbeat_ts) {
    this.name = name;
    this.addr = addr;
    this.state = state;
    this.last_heartbeat_ts = last_heartbeat_ts;
};

function nodeFromRow(row) {
    return new Node(row.name, row.addr, row.state, row.last_heartbeat_ts);
}

module.exports = {
    getNodes: function(status, callback) {
	database.all('SELECT name, addr, last_heartbeat_ts, state FROM nodestate where state = "ACTIVE";',
		function(err, rows) {
		    var nodes = new Array();
		    rows.forEach(function(row) {
			nodes.push(nodeFromRow(row));
		    });
		    callback(nodes);
		});
    },
    updateNode: function(node, callback) {
	var stmt = database.prepare(
	    'INSERT INTO nodestate(name, addr, last_heartbeat_ts, state) ' +
		'VALUES(?, ?, ?, ?);',
	    node.name, node.addr, Date.now(), node.state);
	console.log('Updating node state for ' + node.name + ' from ' + node.addr);
	stmt.run(callback);
    }

};
