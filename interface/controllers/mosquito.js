var mqtt = require('mqtt')
var responses = require('../helper/responses');
var user = require('../controllers/userController');

var options = {
    port: 8083,
    host: 'mqtt://iot.atibha.com',
    clientId: 'mqttjs_' + Math.random().toString(16).substr(2, 8),
    username: 'JDsingh',
    password: 'JDsingh',
    keepalive: 60,
    reconnectPeriod: 1000,
    protocolId: 'MQIsdp',
    protocolVersion: 3,
    clean: true,
    encoding: 'utf8'
};

var client = mqtt.connect('mqtt://iot.atibha.com', options);
client.on('connect', function () { // When connected
    console.log('connected');
});


module.exports.operate = function (req, res) {
    id = req.body.id;
    deviceId = req.body.deviceId;
    val = req.body.val;
    client.publish(topic = deviceId + "/" + id, msg = val)
    if(id === 'all') {
        user.publishAll(deviceId, val)
    } else {
        user.publish(deviceId, id, val)
    }
    return responses.successMsg(res, null);
};