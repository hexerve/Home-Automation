# import time
# import network

# import setup
# import ledSignals
# import homeAutomation

# wlan = network.WLAN(network.STA_IF)
# setup.networkConnect('JDsingh', 'qazxswed')

# while True:

#     # 5.5
#     if not wlan.isconnected():
#         ledSignals.disconnected()
#     else:
#         ledSignals.connected()

#     # 2
#     if setup.isSetupInitiated():
#         setup.configSetup()
#     else:
#         time.sleep(1)


import time
import network
import machine

from lib.umqttRobust import MQTTClient

import setup
import ledSignals
import homeAutomation

wlan = network.WLAN(network.STA_IF)
data = setup.initialize()

isBroker = False

p4 = machine.Pin(4, machine.Pin.OUT)
p4.low()

def sub_cb(topic, msg):
    topic = topic.decode("utf-8")
    msg = msg.decode("utf-8")
    device = (int)(topic.split('/')[1])
    homeAutomation.operate(device, msg)


client = MQTTClient(client_id="esp8266", server="iot.hexerve.com",
                    port=8883, user="JDsingh", password="JDsingh")

client.set_callback(sub_cb)

while not wlan.isconnected():
    # 5.5
    ledSignals.disconnected()

    if data and ('ssid' in data) and ('password' in data):
        setup.networkConnect(data["ssid"], data["password"])

    # 2
    if setup.isSetupInitiated():
        setup.configSetup()
    else:
        time.sleep(1)

while True:
    try:
        client.connect()
        isBroker = True
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
        if data and ('ssid' in data) and ('password' in data):
            setup.networkConnect(data["ssid"], data["password"])
    else:
        ledSignals.connected()
        try: 
            client.connect(False)
            if(not isBroker):
                client.subscribe(topic= data["id"] + "/#")
                isBroker = True                
            client.check_msg()
            p4.low()
        except:
            print("broker disconnected")
            p4.high()
            isBroker = False
        
    # 2
    if setup.isSetupInitiated():
        setup.configSetup()
    else:
        time.sleep(1)

    # client.publish(topic="test", msg="OFF")
    