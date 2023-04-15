import soilSensor
from utils import getIsotime, getConfig, edit_file

from microdot import Microdot
app = Microdot()
config = getConfig()

@app.get('/')
def hello(request):
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
    edit_file('temps.json',obj)
    return 'Soil: ' + str(average(val)) +'\nAt: ' + str(time)

def average(lst):
    return sum(lst) / len(lst)

def start_web_server():
    app.run(debug=True)
    
