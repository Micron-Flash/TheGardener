
import network

wlan = network.WLAN(network.STA_IF)

def connect(config):
    ssid, password = config['ssid'], config['password']
    wlan.active(True)

    max_wait = 10000
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    return True

def disconnect():
    print("disconnecting")
    wlan.disconnect()
