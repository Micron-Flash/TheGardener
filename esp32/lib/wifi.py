
import time
import socket
import sys
import endpoints
import json
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
    wlan.disconnect()

#def decode(ssid, password):
    #decoded_ssid = a2b_base64(ssid).decode()
    #decoded_password = a2b_base64(password).decode()
   # return(decoded_ssid, decoded_password)

def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1] # type: ignore
    s = socket.socket() # type: ignore
    s.bind(addr) 
    s.listen(1)
    print('listening on', addr)

    while True:
        try:
            cl, addr = s.accept()
            print('client connected from', addr)
            request = cl.recv(1024).decode()
            fields = request.split("\r\n")
            info = fields[0].split(' ')
            method = info[0]
            path = info[1]
            fields = fields[1:]
            output = {}
            output["method"] = method
            output["path"] = path
            output["body"] = {}
            for field in fields:
                if not field:
                    continue 
                if is_json(field):
                    print("JSON detected putting it in the body: " + field)
                    output["body"] = field
                else:
                    key,value = field.split(':')
                    output[key] = value
            response = {
                'message': 'No message',
                'code': '500 Error\r\n'
                }
            if output['method'] == 'GET':
                response = endpoints.GET_REQUEST(output)
                cl.send(str('HTTP/1.0 ' + response['code'] + 'Content-type: text/html\r\n\r\n'))
                cl.send(str(response['message']))
            elif output['method'] == 'POST':
                response = endpoints.POST_REQUEST(output, output['body'])
                cl.send(str('HTTP/1.0 ' + response['code'] + 'Content-type: text/html\r\n\r\n'))
                cl.send(str(response['message']))
            cl.close()
        except Exception as e:
            print(e)
            cl.close() # type: ignore
            print('connection closed')
            sys.exit()
            

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True