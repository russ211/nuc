import os

from flask import Blueprint, request, flash, jsonify

from mysite.db import get_db, db_do

bp = Blueprint('station', __name__, url_prefix='/stations')

DES = "/home/kandao/factory"


def mount(username, password, src, des):
    cmd = "mount -t cifs -o username={},password={} {} {}".format(username, password, src, des)
    print(cmd)
    code = os.system(cmd)
    return code


def umount(des):
    cmd = "umount {}".format(des)
    print(cmd)
    code = os.system(cmd)
    print("umount {}".format(code))
    return code


def get_station(uuid):
    station = get_db().execute(
        'SELECT id, ip, uuid, status,src from Stations where uuid = ?', (uuid,)
    ).fetchone()
    return station


@bp.route('/', methods=('GET',))
def index():
    db = get_db()
    stations = db.execute(
        "select id,username,password,ip,uuid,src,des,status,created from Stations order by created desc").fetchall()
    data = [
        {
            'id': s['id'],
            'username': s['username'],
            'password': s['password'],
            'ip': s['ip'],
            'uuid': s['uuid'],
            'src': s['src'],
            'des': s['des'],
            'status': s['status'],
            'created': s['created'].strftime("%Y-%m-%d %H:%M:%S")
        } for s in stations
    ]
    ret = jsonify({'code': 0, 'msg': 'success', "data": data})
    return ret


@bp.route('/register', methods=('POST',))
def register():
    body = request.json
    ip = body.get('ip')
    username = body.get('username')
    password = body.get('password')
    uuid = body.get('uuid')
    src = body.get('src')
    print("request register json: {}".format(body))
    if not ip or not uuid or not src:
        ret = jsonify({"code": -1, "msg": "param error."})
        return ret

    stn = get_station(uuid)
    full_src = "//{}/{}".format(ip, src)
    full_des = os.path.join(DES, uuid)
    if not os.path.exists(full_des):
        os.makedirs(full_des)
    if stn is None:
        code = mount(username, password, full_src, full_des)
        if code == 0:
            action, value = 'INSERT INTO Stations (username,password,ip,uuid,src,des) values (?,?,?,?,?,?)', (
                username, password, ip, uuid, full_src, full_des)
            db_do(action, value)
            ret = jsonify({"code": 0, "msg": "station register success."})
        else:
            ret = jsonify({"code": -1, "msg": "mount error: %d" % code})
    else:
        if stn['ip'] != ip:
            # unmount
            umount(stn['des'])
            # mount
            code = mount(username, password, full_src, full_des)
            if code == 0:
                action, value = 'UPDATE Stations SET username= ?, password= ?, ip=?, src= ?, des= ?  WHERE uuid = ?', (
                    username, password, ip, full_src, full_des, uuid)
                db_do(action, value)
                ret = jsonify({"code": 0, "msg": "station update success."})
            else:
                ret = jsonify({"code": -1, "msg": "mount error: %d" % code})
        else:
            # update status
            if stn["status"] != 1:
                action, value = 'UPDATE Stations SET status = ? WHERE uuid = ?', (1, uuid)
                db_do(action, value)
            ret = jsonify({"code": 0, "msg": "station is good."})
    return ret

# @bp.route('/test', methods=('get',))
# def test():
#     a = os.system("mount -t cifs -o username=russ,password=211 //192.168.41.125/Share /data/share")
#     # ret = a.read()
#     # print(ret)
#     # return ret
#     print(a)
#     return jsonify({"code": a})
