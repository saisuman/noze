var rpc = require('./rpc');
var db = require('./db');

NODE_STATUSES = {
    STATE_ACTIVE: 'ACTIVE',
    STATE_ERROR: 'ERROR',
    STATE_STALE: 'STALE',
    STATE_UNKNOWN: 'UNKNOWN'
};


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
    updateNode: function(payload, callback) {
	console.log('Update request with payload: ' + JSON.stringify(payload));
	if (!isValidNodeStatus(payload)) {
	    callback(rpc.STATUS_REQUEST_ERROR, {});
	    return;
	}
	db.updateNode(payload, function() { callback(rpc.RESPONSE_OK); });
    },

    getNodes: function(payload, callback) {
	db.getNodes(null, function(nodes) {
	    callback(rpc.STATUS_OK, nodes);
	}); 
    }
};
