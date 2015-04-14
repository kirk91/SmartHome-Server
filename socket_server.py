#! /usr/bin/env python
# coding:utf-8

import socket
import json
from rpyc import Service
from rpyc.utils.server import ThreadedServer

import threading
import redis

import config


class RpcService(Service):

    def exposed_handle_msg(self, msg):
        msg_dict = json.loads(msg)
        device_id = msg_dict['device_id']
        sensor_id = msg_dict['sensor_id']
        sensor_value = msg_dict['value']
        if device_id in socket_server.conns and \
                socket_server.conns[device_id]:
            conn = socket_server.conns[device_id]
            req_msg = {"device": device_id,
                       "sensor": sensor_id,
                       "command": sensor_value}
            try:
                conn.send(json.dumps(req_msg))
                return True
            except Exception, e:
                print e
                conn.close()
                socket.server.conns.pop(device_id)
                return False
        else:
            return False


class SocketServer(threading.Thread):

    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ss.bind((host, port))
        self.ss.listen(100)
        self.conns = {}
        self.redis = redis.Redis(
            host=config.redis_host, port=config.redis_port, db=config.redis_db)

    def serve(self):
        print "socket_server starting...\n"
        while True:
            conn, addr = self.ss.accept()
            login_msg = conn.recv(2048)
            try:
                login_msg = json.loads(login_msg)
                device_id = int(login_msg['device_id'])
                info = login_msg['info']
                if info == 'login' and \
                        self.redis.sismember('device:list', device_id):
                    # 将conn与device_id 对应起来
                    self.conns[device_id] = conn
                    response = {
                        'status': 0, 'err_msg': '', 'info': "Login Success"}
                    conn.send(json.dumps(response))
                else:
                    response = {'status': -1,
                                'err_msg': 'invalid device_id',
                                'info': 'Login error'}
                    conn.send(json.dumps(response))
            except Exception, e:
                print e

    def close(self):
        # 关闭客户端连接
        for key in self.clients.keys():
            try:
                self.conns[key].close()
            except Exception, e:
                print e
        self.ss.close()

    def run(self):
        self.serve()


class RpcServer(ThreadedServer):

    def __init__(self, *args, **kwargs):
        ThreadedServer.__init__(self, *args, **kwargs)

    def start(self):
        print "rpc_server starting...\n"
        ThreadedServer.start(self)

socket_server = SocketServer('0.0.0.0', 8888)
socket_server.setDaemon(True)
rpc_server = RpcServer(RpcService, port=8889, auto_register=False)


def main():
    socket_server.start()
    rpc_server.start()

if __name__ == '__main__':
    main()
