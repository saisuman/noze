var sqlite3 = require('sqlite3').verbose();
module.exports = {
    connect: function(fileName) {
	return new sqlite3.Database(fileName);
    },
    getActiveNodes: function(db) {
	db.each('SELECT name, addr, last_heartbeat_ts, state FROM nodestate;"',
		function(err, row) {
		    console.log(row.name, row.addr);
		});
    }
};
