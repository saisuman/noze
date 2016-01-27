module.exports = {
    getActionPayload: function(req) {
	if (req.query.payload) {
	    return null;
	}
	try {
	    return eval("(" + unescape(req.query.payload) + ")");
	} catch(err) {
	    console.log('Invalid request:', req);
	    return null;
	}
    },

    sendResponse: function(payload, res) {
	return JSON.stringify(payload);
    }
};
