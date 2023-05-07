
import network

CLIENT_ID = 'gardenbot'
wlan = network.WLAN(network.STA_IF)


def connect(config):
    ssid, password = config['ssid'], config['password']
    wlan.active(True)
    max_wait = 10000
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.config(dhcp_hostname=CLIENT_ID)
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
