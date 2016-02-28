function toRelTime(epochMilliseconds) {
    var diffMinutes = parseInt((Date.now() - epochMilliseconds) / 1000 / 60);
    if (diffMinutes > 100) {
	var diffHours = parseInt(diffMinutes / 60);
	return diffHours + ' hours ago';
    }
    return diffMinutes + ' minutes ago';  
}

function drawNodeTable(responseObj) {
    var table = document.getElementById('nodetable');
    // Remove all but header.
    for (var i = 1, l = table.children.length; i < l; ++i) {
	table.removeChild(table.children[i]);
    }
    if (responseObj.status != 'OK') {
	return;
    }
    responseObj.payload.forEach(function addRow(node) {
	var row = document.createElement('tr');
	function addCol(value) {
	    var col = document.createElement('td');
	    col.innerHTML = value;
	    row.appendChild(col);
	};
	addCol(node.name);
	addCol(node.addr);
	addCol(toRelTime(node.last_heartbeat_ts));
	addCol(node.state);
	table.appendChild(row);
    });
}

function init() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
	if (xhttp.readyState == 4 && xhttp.status == 200) {
	    var responseObj = eval("(" + xhttp.responseText + ")");
	    drawNodeTable(responseObj);
	}
    };
    xhttp.open("GET", "/action_query", true);
    xhttp.send();
}
