import soilSensor
from utils import getIsotime, getConfig
from machine import Pin
import time
import json

from microdot import Microdot, send_file
app = Microdot()
config = getConfig()

@app.get('/dashboard')
def dashboard(request):
    return send_file('/static/index.html')

@app.get('/garden.png')
def dashboard(request):
    return send_file('/static/garden.png')

@app.get('/favicon.ico')
def favicon(request):
    return send_file('/static/garden.png')

@app.post('/updateConfig')
def updateConfig(request):
    print(request.json)
    with open('/config.json', 'w') as newConfig:
        json.dump(request.json, newConfig)
    newConfig.close()
    return 'Okay'

@app.get('/config.json')
def returnConfig(request):
    return getConfig()

@app.get('/')
def hello(request):
    p0 = Pin(12, Pin.OUT)
    p0.on()       
    time.sleep(30)
    p0.off()
    return 'Hello world'

@app.get('/soil')
def soil(request):
    sample_size = 10
    for i in range(sample_size): 
        val = []
        val.append(soilSensor.read())
    time = getIsotime()
    obj = {
        "temp": average(val),
        "time": str(time)
    }
    return obj

def average(lst):
    return sum(lst) / len(lst)

def start_web_server():
    app.run(port=80, debug=True)
    
