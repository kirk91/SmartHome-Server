# coding:utf-8

import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, Aws')


class ErrorHandler(tornado.web.RequestHandler):
    CLIENT_ERROR = 101

    def get(self, errcode):
        if errcode == self.CLIENT_ERROR:
            content = '您还未绑定任何设备, 请绑定设备后重试'
        else:
            content = '未知错误'
        self.render('error.html', content=content)


class Testhandler(tornado.web.RequestHandler):
    '''
    '''

    def get(self):
        self.render('test/test.html')