import time
import machine

p2 = machine.Pin(2, machine.Pin.OUT)
p2.high()

p5 = machine.Pin(5, machine.Pin.OUT)
p5.high()

p3 = machine.Pin(3, machine.Pin.OUT)
p3.high()

p15 = machine.Pin(15, machine.Pin.OUT)
p15.high()

p13 = machine.Pin(13, machine.Pin.OUT)
p13.high()

p12 = machine.Pin(12, machine.Pin.OUT)
p12.high()

p14 = machine.Pin(14, machine.Pin.OUT)
p14.high()


def dot():
    p2.low()
    time.sleep(0.5)
    p2.high()
    time.sleep(0.5)


def dash():
    p2.low()
    time.sleep(2)
    p2.high()
    time.sleep(0.5)


def red():
    p3.low()
    time.sleep(0.5)
    p3.high()


def green():
    p12.low()
    time.sleep(0.5)
    p12.high()
    time.sleep(0.5)
    p12.low()
    time.sleep(0.5)
    p12.high()
    time.sleep(0.5)
    p12.low()
    time.sleep(0.5)
    p12.high()


def blue():
    p14.low()
    time.sleep(0.5)
    p14.high()


def white():
    p15.low()
    time.sleep(1)
    p15.high()


def blueMid():
    p13.low()
    time.sleep(1)
    p13.high()


def on():
    p5.low()

def off():
    p5.high()