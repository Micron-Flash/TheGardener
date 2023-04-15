from utils import setRTC
from esp32.wifi import disconnect
from endpointsV2 import start_web_server
from gc import mem_free, collect

if __name__ == "__main__":
    collect()
    mem_free()
    from utils import setRTC
    from esp32.wifi import disconnect
    from endpointsV2 import start_web_server
    setRTC()
    start_web_server()
