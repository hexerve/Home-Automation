import machine

pins = [
    machine.Pin(14, machine.Pin.OUT), machine.Pin(12, machine.Pin.OUT), machine.Pin(
        13, machine.Pin.OUT), machine.Pin(15, machine.Pin.OUT), machine.Pin(3, machine.Pin.OUT)
]

for pin in pins:
    pin.low()

def operate(num, msg):
    if(msg == 'ON'):
        pins[num].high()
    if(msg == 'OFF'):
        pins[num].low()

    print(num, msg)
