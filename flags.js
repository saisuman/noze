var cmdLineArgs = require('command-line-args');
var args = cmdLineArgs([
    { name: 'port', alias: 'p', type: Number, defaultValue: 8090 },
    { name: 'databaseFile', alias: 'd', type:String, defaultValue: 'noze.db'}
]);
module.exports = args.parse();
