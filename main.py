import time
import network    

from lib.umqttRobust import MQTTClient

import setup
import ledSignals

wlan = network.WLAN(network.STA_IF)
data = setup.initialize()

def sub_cb(topic, msg):
    if topic == b'JDchauhan/feeds/lights':
        if msg == b'ON':
            ledSignals.on()
        elif msg == b'OFF':
            ledSignals.off()
        else: print(msg)
    else:
        print("topic:", topic)
        print("msg:", msg)
        

# client = MQTTClient("device_id", "io.adafruit.com",user="JDchauhan", password="d676d8ed600b44a58d737f732cfd7440")
# client = MQTTClient("device_id", "iot.hexerve.com",user="JDsingh", password="JDsingh")
# client = MQTTClient(client_id = "esp8266", server = "iot.hexerve.com", port = 8083, user = b"JDsingh", password = b"JDsingh")
client = MQTTClient(client_id = "esp8266", server = "iot.hexerve.com", port = 8083, user = "JDsingh", password = "JDsingh")

client.set_callback(sub_cb)
client.connect()
# client.subscribe(topic="JDchauhan/feeds/lights")

while True:
    
    # # 5.5
    # if not wlan.isconnected():
    #     ledSignals.red()
    #     if data and data["ssid"] and data["password"]:
    #         setup.networkConnect(data["ssid"], data["password"])
    # else:
    #     ledSignals.blue()
    #     client.check_msg()
            

    # # 2
    # if setup.isSetupInitiated():
    #     setup.configSetup()
    # else: time.sleep(1)

    client.publish(topic="test", msg="OFF")