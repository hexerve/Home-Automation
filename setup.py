import network
import socket
import json
import time
import machine
import ledSignals

def initialize():
    f = open("config.txt", "r")
    data = json.loads(f.read())
    f.close()
    return data

def configSetup():

    htmlData = """<!DOCTYPE html>
    <html>
        <head> 
            <title>Home Automation</title> 
        </head>
        <body> 
            <h1>Home Automation</h1>
            <div id="err" style="background: #FFA6A6">
            </div>
            <br/>
            <form method="GET" action="\login">
                <input type='text' id='name' name='ssid' placeholder='SSID/ wifi name'/>
                <input type='password' id='password' name='password' placeholder='Password'/>
                <input type='submit' value='Submit' />
            </form>
        </body>
    </html>
    """

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

    while True:
        cl, addr = s.accept()
        data = cl.recv(4096)
        
        if data:
            method, path, protocol = data.decode().strip().split('\n')[0].split(' ')
            
            if method == 'GET':
                if path == '/':
                    response = htmlData
                elif path.split('?')[0] == '/login':
                    d1, d2 = path.split('?')[1].split('&')
                    if d1 and d2:
                        ssid = d1.split('=')[1]
                        password = d2.split('=')[1]
                        response = 'success';
                        cl.send(response.encode('utf-8'))
                        cl.shutdown(socket.SHUT_RDWR)
                        cl.close()
                        break;
                else:
                    response = 'error'
            else: 
                response = 'err'
            
        cl.send(response.encode('utf-8'))
        cl.close()
    
    testCredentials(ssid, password)

def saveCredentials(ssid, password): 
    f = open('config.txt', "w")
    f.write('{"ssid": "' + ssid + '", "password": "' + password + '"}')
    f.close()


def testCredentials(ssid, password):
    networkDisconnect()

    isConnected = False
    for _ in range(3):
        networkConnect(ssid, password)
        if isNetwork():
            isConnected = True
            break

    if isConnected: 
        # ledSignals.dot()
        # ledSignals.dot()
        # ledSignals.dot()
        # ledSignals.dot()
        
        ledSignals.green()

        print("Saving Credentials")
        saveCredentials(ssid, password)

    else:
        # ledSignals.dash()
        # ledSignals.dot()
        # ledSignals.dash()

        ledSignals.red()
    

def isNetwork():
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        print("connected") 
        ledSignals.blue()
        # ledSignals.dash()
        # ledSignals.dash()
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
        # ledSignals.dot()
        ledSignals.white()
        time.sleep(5)
    else: 
        print("already connected")
        ledSignals.green()


def networkDisconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    # ledSignals.dash()
    ledSignals.blueMid()
    print('disconnected from network...')


def isSetupInitiated():
    p = machine.Pin(4, machine.Pin.IN)
    print("pin"p.value())
    if not p.value():
        time.sleep(2)
        if not p.value():
            return True
        return False
    return False