from flask import jsonify, current_app, request
import json
import threading


from . import api
from ..tools import updater
from .. import socketio
from ..models import Report, User
from .. import db

from ..tools.read import read_relays


@api.route('/relays')
def relays():
    content = json.loads(open("details").read())
    data = list()
    for item in content['relays']:
        try:
            data.append([item['longitude'], item['latitude'], item['or_addresses'][0].split(':')[0], item['country'],
                         item['running']])
        except:
            data.append([-360, -360, item['or_addresses'][0].split(':')[0], 'unknown', item['running']])
    # data = [[0, 0]]
    # data.append([50,50,"192.168.1.1","CN",True])
    d = threading.Thread(target=updater.download)
    d.start()
    return jsonify({"relays": data, "time": content['relays_published']}), {"Content-Range": "0-%d/%d" % (len(data), len(data))}
#
#
# @api.route('/notify')
# def get_notify():
#     payload = dict()
#     payload['data'] = [(1, '欢迎使用本系统', False), [2, '上次更新结点时间 2017-9-28', False], (3, '发现新结点', True)]
#     return jsonify(payload), {"Content-Range": "0-%d/%d" % (len(payload['data']), len(payload['data']))}


@api.route('/add_notify/')
def add_notify():
    data, time = read_relays()
    socketio.emit("update", {"relays": data, "time": time}, namespace='/relays', broadcast=True)
    return jsonify({"relays": data, "time": time})


@api.route('/report')
def get_report():
    range = json.loads(request.args.get('range', default='[0,24]'))
    data = Report.query.order_by(Report.time.desc())
    size = len(data.all())
    result = []
    for item in data.offset(range[0]).limit(range[1]-range[0]).all():
        result.append(item.as_dict())
    return jsonify(result), {"Content-Range": "%d-%d/%d" % (range[0], range[0] + len(result), size)}
