import time
import machine

p5 = machine.Pin(5, machine.Pin.OUT)
p5.low()

p4 = machine.Pin(4, machine.Pin.OUT)
p4.low()

p2 = machine.Pin(2, machine.Pin.OUT)
p2.low()

def connected():
    p5.high()
    time.sleep(0.1)
    p5.low()
    time.sleep(0.1)

def save():
    p5.high()
    time.sleep(0.1)
    p5.low()
    time.sleep(0.1)
    p5.high()
    time.sleep(0.1)
    p5.low()
    time.sleep(0.1)
    p5.high()
    time.sleep(0.1)
    p5.low()
    
def disconnecting():
    p4.high()
    time.sleep(0.1)
    p4.low()
    time.sleep(0.1)
    p4.high()
    time.sleep(0.1)
    p4.low()
    time.sleep(0.1)
    p4.high()
    time.sleep(0.1)
    p4.low()
    
def disconnected():
    p4.high()
    time.sleep(0.1)
    p4.low()
    
def connecting():
    p2.high()
    time.sleep(0.1)
    p2.low()