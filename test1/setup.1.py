# import network
import socket
import json
# import urllib.parse 

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
            <form method="POST" action="\login">
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
                # if path == '/':
                    response = htmlData
                    # elif path.split('?')[0] == '/login':
                    #     d1, d2 = path.split('?')[1].split('&')
                    #     if d1 and d2:
                    #         ssid = urllib.parse.unquote(d1.split('=')[1])
                    #         password = urllib.parse.unquote(d2.split('=')[1])
                    #         response = 'success';
                    #         print(ssid)
                    #         print(password)
                    #         # saveCredentials(ssid, password, False)
                    #     else:
                    #         response = 'error'
                # else: 
                #     response = 'err'
            elif method == 'POST':
                print(data)
                #     # postData = data.decode()[data.decode().find('{'):]
                #     # import json
                #     # postData= json.loads(postData)
                #     # print(postData)
                # print(postData['devices'])

                response = htmlData
            else : 
                response = 'err'
            
        cl.send(response.encode('utf-8'))
        cl.close()


def saveCredentials(ssid, password, isTested):
    if isTested:
        name = 'config.txt'
    else:
        name = 'test_config.txt' 
    f = open(name, "w")
    f.write('{"ssid": "' + ssid + '", "password": "' + password + '"}')
    f.close()
    if not isTested:
        testCredentials()


def testCredentials():
    networkDisconnect()

    f = open("test_config.txt", "r")
    data = json.loads(f.read())
    f.close()

    isConnected = False
    for _ in range(3):
        if(networkConnect(data["ssid"], data["password"])):
            isConnected = True
            break

    if isConnected: 
        saveCredentials(data["ssid"], data["password"], True)
    else:
        f = open("test_config.txt", "r")
        data = json.loads(f.read())
        f.close()
        if data["ssid"] and data["password"]:
            networkConnect(data["ssid"], data["password"])

def networkConnect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            blink_led(0, 0, 255)
            return False
    print('connected to network...')
    print('network config:', wlan.ifconfig())
    blink_led(0, 255, 255)
    return True


def networkDisconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    blink_led(128, 128, 0)
    print('disconnected from network...')