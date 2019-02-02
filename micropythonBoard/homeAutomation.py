import machine
import json

pins = [
    machine.Pin(14, machine.Pin.OUT), machine.Pin(12, machine.Pin.OUT), machine.Pin(
        13, machine.Pin.OUT), machine.Pin(15, machine.Pin.OUT), machine.Pin(3, machine.Pin.OUT)
]

for pin in pins:
    pin.low()

with open("automation.json", "r") as jsonFile:
    data = json.load(jsonFile)
    for i in range (0,5):
        if (data[str(i)] == 0):
            pins[i].low()
        else:
            pins[i].high()


def operateAll(msg):
    data = {}

    if(msg == 'ON'):
        for i in range (0,5):    
            data[str(i)] = 1
            pins[i].high()
    else:
        for i in range (0,5):    
            data[str(i)] = 0
            pins[i].low()

    data = json.dumps(data)

    print(data)
    f = open('automation.json', "w")
    f.write(data)
    f.close()

    print("all", msg)


def operate(num, msg):
    with open("automation.json", "r") as jsonFile:
        data = json.load(jsonFile)

    if(msg == 'ON'):
        data[str(num)] = 1
        pins[num].high()

    if(msg == 'OFF'):
        pins[num].low()
        data[str(num)] = 0

    data = json.dumps(data)

    print(data)
    f = open('automation.json', "w")
    f.write(data)
    f.close()

    print(num, msg)


