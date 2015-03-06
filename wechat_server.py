#! /usr/bin/env python
# coding:utf-8

import tornado.ioloop
import tornado.httpserver
import tornado.options

import sys
sys.path.append("libs")

from application import app
import config

from tornado.options import define,options
define("port",default=8887,help="wechat_server run on the given port",type=int)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
