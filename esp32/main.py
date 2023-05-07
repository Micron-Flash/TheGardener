from utils import setRTC
from wifi import disconnect
from gc import mem_free, collect
from endpointsV2 import start_web_server
    
if __name__ == "__main__":
    collect()
    mem_free()
    start_web_server()
