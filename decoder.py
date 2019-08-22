import socket
import json
import struct
import asterix
import uvicorn
from threading import Thread
from mess import Mess
# socketio
import socketio
sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'app.html'},
})
background_task_started = False
background_search_started = False
global msg
msg = '[{}' 
async def background_task():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        # thread.start_new_thread(search, ('test.log'), {"id": 1})
        # search('test.log')
        # background_search_started = True
        await sio.sleep(1)
        count += 1
        global msg
        await sio.emit('data',msg+']',namespace='/test')
        msg = '[{}'
        
@sio.on('connect', namespace='/test')
async def test_connect(sid, environ):
    global background_task_started
    if not background_task_started:
        sio.start_background_task(background_task)
        background_task_started = True

@sio.on('disconnect', namespace='/test')
def test_disconnect(sid):
    print('Client disconnected')

def udpInit():
    # socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 9999)) # 广播方式

    # mess = ''
    # data_rest = None
    while True:
        data = sock.recv(100)
        # print('----------------------')
        # Parse data verbose=False
        parsed = asterix.parse(data, verbose=False)
        # for packet in parsed:
        #     for item in packet.items():
        #         print(item)
        # print('----------------------')
        mess = Mess(parsed)
        mess.getData()
        mess.parsed = ''
        in_json = json.dumps(mess.__dict__) 
        # print(in_json)
        global msg
        msg += ',' + in_json

if __name__ == '__main__':
    thread_01 = Thread(target=udpInit)
    thread_01.start()
    uvicorn.run(app, host='127.0.0.1', port=5012)