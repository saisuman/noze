var google = require('googleapis');
var fs = require('fs');
var atob = require('atob');
var auth = require('./googleauth');

function processAttachment(auth, messageId, attachmentId) {
    var gmail = google.gmail('v1');
    gmail.users.messages.attachments.get({
	id: attachmentId,
	userId: 'me',
	messageId: messageId,
	auth: auth
    }, function(err, response) {
	if (err) {
	    console.log('ERROR: Could not get attachment.', err);
	    return;
	}
	var fileName = messageId + '.attachment';
	fs.writeFile(fileName, JSON.stringify(response), function(err) {
	    if (err) {
		console.log('ERROR: Could not write.', err);
		return;
	    }
	    console.log('Wrote file into: ', fileName);
	});
	fs.writeFile(fileName + '.data', atob(response.data));
    });	
}

function processMessage(auth, mailMessage) {
    console.log('Processing email ID: ', mailMessage.id);
    var gmail = google.gmail('v1');
    gmail.users.messages.get({
	auth: auth,
	userId: 'me',
	format: 'full',
	id: mailMessage.id
    }, function(err, response) {
	// Let's go through the response and see if there are any
	// non-zero sized parts.
	for (var i in response.payload.parts) {
	    var part = response.payload.parts[i];
	    var body = part.body;
	    if (body.size > 0 ) {
		console.log('Found an attachment: ', body.size,
			    ' bytes, type ',  part.mimeType,
			    'attachmentId: ', body.attachmentId);
		processAttachment(auth, mailMessage.id, body.attachmentId);
	    }
	    
	}

    });
}

function findMailsFromScanner(auth) {
    var gmail = google.gmail('v1');
    gmail.users.messages.list({
	auth: auth,
	userId: 'me',
	q: 'to:home+scan@saisuman.com is:unread'
    }, function(err, response) {
	if (err) {
	    console.log('The API returned an error: ' + err);
	    return;
	}
      var messages = response.messages;
	if (messages.length == 0) {
	    console.log('No messages found.');
	    return;
	}
	console.log(':');
	for (var i = 0; i < messages.length; i++) {
	    processMessage(auth, messages[i]);
	}
    });
}

auth.authAndRun(findMailsFromScanner);
