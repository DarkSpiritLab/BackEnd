from .. import socketio
from flask import request, current_app
from flask_socketio import emit
from ..tools import updater
from ..tools.read import read_relays
import threading


@socketio.on('connect', namespace='/notifies')
def notify_connect():
    emit('notify_list', {'data': [(1, '欢迎使用本系统', False), [2, '上次更新结点时间 2017-9-28', False], (3, '发现新结点', True)]})
    try:
        current_app.sid.append(request.sid)
    except:
        current_app.sid = [request.sid]


@socketio.on('disconnect', namespace='/notifies')
def test_disconnect():
    print('Client disconnected')
    current_app.sid.remove(request.sid)


@socketio.on('get_notify', namespace='/notifies')
def get_notify(data):
    print(data)
    emit('notify_list', {'data': [(1, '欢迎使用本系统', False), [2, '上次更新结点时间 2017-9-28', False], (3, '发现新结点', True)]})


@socketio.on('get', namespace='/relays')
def get_relays():
    data, time = read_relays()
    # d = threading.Thread(target=updater.download, args=[request.sid])
    # d.start()
    emit('update', {"relays": data, "time": time})
    socketio.start_background_task(target=updater.download)



