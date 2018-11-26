'use strict';
var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var Values = new Schema({
  0: {
    type: Boolean,
    default: false
  },
  1: {
    type: Boolean,
    default: false
  },
  2: {
    type: Boolean,
    default: false
  },
  3: {
    type: Boolean,
    default: false
  },
  4: {
    type: Boolean,
    default: false
  },
});

var Devices = new Schema({
  deviceId: {
    type: String
  },
  name: {
    type: String,
    default: "Device_" + new Date().getTime()
  },
  values: Values,
  user: {
    type: Schema.Types.ObjectId,
    ref: 'users'
  },
});

module.exports = mongoose.model('device', Devices, 'devices');