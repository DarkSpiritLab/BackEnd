import urllib3
import os
from .. import socketio
from ..tools.read import read_relays
from time import sleep


def download():
    if not os.path.exists('details.lock'):
        with open('details.lock', 'w') as f:
            f.write('1')
        print('start fetch')
        http = urllib3.ProxyManager("http://127.0.0.1:8001")
        r = http.request('GET', 'https://onionoo.torproject.org/details')
        # r = http.request('GET', 'http://acg.nadc.cn')
        file = open("details", 'w')
        file.write(bytes.decode(r.data))
        os.remove('details.lock')
        print('fetch success!')
    else:
        print('resources locked!')
    sleep(10)
    print('write')
    data, time = read_relays()
    socketio.emit("update", {"relays": data, "time": time}, namespace='/relays')
