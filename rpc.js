Response = function(status, payload) {
    this.status = status;
    this.payload = payload;
};

var STATUS_OK = 'OK';
var STATUS_SERVER_ERROR = 'SERVER_ERROR';
var STATUS_REQUEST_ERROR = 'REQUEST_ERROR';
var STATUS_TRANSIENT_ERROR = 'TRANSIENT_ERROR';

var RESPONSE_OK = new Response(STATUS_OK);
var RESPONSE_SERVER_ERROR = new Response(STATUS_SERVER_ERROR);
var RESPONSE_REQUEST_ERROR = new Response(STATUS_REQUEST_ERROR);
var RESPONSE_TRANSIENT_ERROR = new Response(STATUS_TRANSIENT_ERROR);

module.exports = {

    STATUS_OK: STATUS_OK,
    STATUS_SERVER_ERROR: STATUS_SERVER_ERROR,
    STATUS_REQUEST_ERROR: STATUS_REQUEST_ERROR,
    STATUS_TRANSIENT_ERROR: STATUS_TRANSIENT_ERROR,

    RESPONSE_OK: RESPONSE_OK,
    RESPONSE_SERVER_ERROR: RESPONSE_SERVER_ERROR,
    RESPONSE_REQUEST_ERROR: RESPONSE_REQUEST_ERROR,
    RESPONSE_TRANSIENT_ERROR: RESPONSE_TRANSIENT_ERROR,

    getActionPayload: function(req) {
	if (!req.query.payload) {
	    return null;
	}
	try {
	    var payload = eval("(" + unescape(req.query.payload) + ")");
	    console.log('Got payload: ' + JSON.stringify(payload));
	    return payload;
	} catch(err) {
	    console.log('Invalid request:', req.query);
	    return null;
	}
    },

    sendResponse: function(status, payload, res) {
	if (!status) {
	    res.send(JSON.stringify(RESPONSE_SERVER_ERROR));
	    return;
	}
	var responseObj = new Response(status, payload);
	res.send(JSON.stringify(responseObj));
	console.log('Sent response: ' + JSON.stringify(responseObj));
    }
};
