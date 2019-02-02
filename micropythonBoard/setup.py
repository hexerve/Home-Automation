import network
import socket
import json
import time
import machine
import ledSignals


def initialize():
    with open("config.json", "r") as jsonFile:
        data = json.load(jsonFile)
    return data


def configSetup():
    p2 = machine.Pin(2, machine.Pin.OUT)
    p2.high()
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

    while True:
        cl, addr = s.accept()
        data = cl.recv(4096)
        response = 'here'
        if data:
            method, path, protocol = data.decode().strip().split('\n')[
                0].split(' ')

            if method == 'POST':
                print('Post')
                x = data.decode()

                while not x[len(data) - 1:] == '}':
                    data += cl.recv(4096)
                    x = data.decode()
                x = None
                
                data = data.decode().strip().split('\n')
                data = data[len(data) - 1]
                data = json.loads(data)

                ssid = data['ssid']
                password = data['password']

                with open("config.json", "r") as jsonFile:
                    data = json.load(jsonFile)

                response = "\r\n"
                response += data["id"]

                cl.send('HTTP/1.0 200 OK\r\n')
                cl.send('Cache-Control: no-cache\r\n')
                cl.send('Access-Control-Allow-Origin: *\r\n')
                cl.send('Access-Control-Allow-Methods: GET, POST, PUT, DELETE\r\n')
                cl.send('Access-Control-Allow-Headers: X-Requested-With,content-type, Authorization\r\n')
                cl.send('Access-Control-Allow-Credentials: true\r\n')
                cl.send(response.encode('utf-8'))

                # cl.shutdown(socket.SHUT_RDWR)
                cl.close()
                testCredentials(ssid, password)
                p2.low()
                break

        cl.send('HTTP/1.0 200 OK\r\n')
        cl.send('Cache-Control: no-cache\r\n')
        cl.send('Access-Control-Allow-Origin: *\r\n')
        cl.send('Access-Control-Allow-Methods: GET, POST, PUT, DELETE\r\n')
        cl.send(
            'Access-Control-Allow-Headers: X-Requested-With,content-type, Authorization\r\n')
        cl.send('Access-Control-Allow-Credentials: true\r\n')

        cl.send(response.encode('utf-8'))
        cl.close()


def saveCredentials(ssid, password):
    with open("config.json", "r") as jsonFile:
        data = json.load(jsonFile)
    
    data["ssid"] = ssid
    data["password"] = password
    
    data = json.dumps(data)

    print(data)
    f = open('config.json', "w")
    f.write(data)
    f.close()

    print("saved") 

def testCredentials(ssid, password):
    networkDisconnect()
    isConnected = False
    for _ in range(3):
        networkConnect(ssid, password)
        if isNetwork():
            isConnected = True
            break

    if isConnected:
        ledSignals.save()
        print("Saving Credentials")
        saveCredentials(ssid, password)

    else:
        ledSignals.disconnected()

    print("reset")
    machine.reset()


def isNetwork():
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        print("connected")
        ledSignals.connected()        
        print('network config:', wlan.ifconfig())
        return True
    else:
        print("not connected")
        return False


def networkConnect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        print(ssid, password)
        wlan.connect(ssid, password)
        ledSignals.connecting()
        time.sleep(5)
    else:
        print("already connected")
        ledSignals.save()


def networkDisconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    ledSignals.disconnecting()
    print('disconnected from network...')


def isSetupInitiated():
    p = machine.Pin(1, machine.Pin.IN)
    print("pin", p.value())
    if not p.value():
        return True
    return False
