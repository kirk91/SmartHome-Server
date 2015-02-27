import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import config
import hashlib
import logging

from tornado.options import define,options
define("port",default=80,help="run on the given port",type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        echostr = self.get_argument('echostr','')
        if self.checkSignature() and echostr:
            self.write(echostr)
        else:
            self.write('hello,world')

    def post(self):
        if self.checkSignature():
            #handle message
            logging.info(self.request.body)
            self.write(self.request.body)
        else:
            self.write('hello,world')

    def checkSignature(self):
        signature = self.get_argument('signature','')
        nonce = self.get_argument('nonce','')
        timestamp = self.get_argument('timestamp','')
        tmp_list = [config.token,timestamp,nonce]
        tmp_list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, tmp_list)
        hash_code = sha1.hexdigest()
        if hash_code== signature:
            return True
        else:
            return False


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/",IndexHandler)],debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
