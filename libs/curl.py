import pycurl
import StringIO
import urllib

class CurlHelper(object):
    """CurlHelper"""
    def __init__(self):
        self.curl = pycurl.Curl()
        self.b = StringIO.StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, self.b.write)
        self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
        self.curl.setopt(pycurl.MAXREDIRS, 5)
        self.curl.setopt(pycurl.CONNECTTIMEOUT, 100)
        self.curl.setopt(pycurl.TIMEOUT, 500)
        self.curl.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36")

    def get(self,url,params=None):
        if params:
            url = url % params
        self.curl.setopt(pycurl.URL, url)
        self.curl.perform()
        return self.b.getvalue()

    def post(self,url,params=None,data=""):
        if params:
            url = url % params
        self.curl.setopt(pycurl.POSTFIELDS, data)
        self.curl.setopt(pycurl.URL, url)
        self.curl.perform()
        return self.b.getvalue()


