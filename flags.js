var cmdLineArgs = require('command-line-args');
var args = cmdLineArgs([
    { name: 'port', alias: 'p', type: Number, defaultValue: 8090 },
    { name: 'databaseFile', alias: 'd', type:String, defaultValue: 'noze.db'},
    { name: 'broadcastPort', alias: 'b', type:Number, defaultValue: 9090},
]);
module.exports = args.parse();
