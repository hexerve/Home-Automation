import time
import network
import machine

from lib.umqttRobust import MQTTClient

import setup
import ledSignals
import homeAutomation


isBroker = True

wlan = network.WLAN(network.STA_IF)
data = setup.initialize()

p4 = machine.Pin(4, machine.Pin.OUT)
p4.low()

def sub_cb(topic, msg):
    topic = topic.decode("utf-8")
    msg = msg.decode("utf-8")
    device = topic.split('/')[1]

    if (device == 'all'):
        homeAutomation.operateAll(msg)
    
    else:
        device = (int) (device)
        homeAutomation.operate(device, msg)
    
    client.check_msg()

# client = MQTTClient(client_id="esp8266", server="iot.atibha.in",
#                     port=8083, user="JDsingh", password="JDsingh")

client = MQTTClient(client_id="esp8266", server="atibha.in", port=8883, user="Hexerve", password="Hexerve")

client.set_callback(sub_cb)

while not wlan.isconnected():
    # 5.5
    ledSignals.disconnected()

    if data and ('ssid' in data) and ('password' in data):
        setup.networkConnect(data["ssid"], data["password"])


    if setup.isSetupInitiated():
        setup.configSetup()
    else:
        time.sleep(1)

while True:
    try:
        client.connect()
        p4.low()
        break
    except :
        p4.high()
        print("error connecting broker")
        pass    

client.subscribe(topic= data["id"] + "/#")    

while True:

    # 5.5
    if not wlan.isconnected():
        ledSignals.disconnected()
        isBroker = False
        if data and ('ssid' in data) and ('password' in data):
            setup.networkConnect(data["ssid"], data["password"])
    else:
        ledSignals.connected()

        for _ in range(3): 
            try:
                client.publish(topic="test", msg="testing")
                if not isBroker:
                    client.subscribe(topic= data["id"] + "/#")                     
                print("connected")
                client.check_msg()
                p4.low()
                time.sleep(0.5)
            except:
                isBroker = False
                print("broker disconnected")
                p4.high()
                time.sleep(2)
                break
            
    if setup.isSetupInitiated():
        setup.configSetup()
