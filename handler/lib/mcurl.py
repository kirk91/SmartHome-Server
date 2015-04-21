# coding:utf-8

import pycurl
import StringIO
import json


class CurlHelper(object):

    """CurlHelper"""

    def __init__(self):
        self.curl = pycurl.Curl()
        # self.curl.setopt(pycurl.VERBOSE, 1)
        self.curl.setopt(pycurl.MAXREDIRS, 5)
        self.curl.setopt(pycurl.CONNECTTIMEOUT, 100)
        self.curl.setopt(pycurl.TIMEOUT, 1000)
        self.curl.setopt(
            pycurl.USERAGENT, '''Mozilla/5.0 (Macintosh; Intel Mac OS X
                10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.
        0.2214.111 Safari/537.36''')

    def get(self, url, params=None, resp_type=None):
        if params:
            url = url % params
        if isinstance(url, unicode):
            url = url.encode('utf-8')
        self.curl.setopt(pycurl.URL, url)
        b = StringIO.StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, b.write)
        self.curl.perform()
        res = b.getvalue()
        b.close()
        if resp_type == 'json':
            return json.loads(res)
        return res

    def post(self, url, params=None, data="", resp_type=None):
        if params:
            url = url % params
        if isinstance(url, unicode):
            url = url.encode('utf-8')
        self.curl.setopt(pycurl.URL, url)
        self.curl.setopt(pycurl.POSTFIELDS, data)
        b = StringIO.StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, b.write)
        self.curl.perform()
        res = b.getvalue()
        b.close()
        if resp_type == 'json':
            return json.loads(res)
        return res

    def close(self):
        self.curl.close()
