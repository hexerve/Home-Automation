'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var Devices = new Schema({
  deviceId: {
    type: String
  },
  name: {
    type: String,
    default: "Device_" + Math.floor(Math.random() * 100000000)
  },
  value: {
    type: Number
  }
});

module.exports = mongoose.model('user', Devices, 'users');