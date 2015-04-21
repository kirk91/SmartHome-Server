# coding:utf-8

import tornado.web
import random
import string
import logging

from .. import config
from ..lib import mcurl


class OauthHandler(tornado.web.RequestHandler):
    '''
    '''

    def get(self):
        redirect_uri = \
            config.wx_oauth_uri % (
                config.appid, config.wx_redirect_uri,
                config.wx_snsapi_base, random.choice(string.digits)
            )
        self.redirect(redirect_uri)


class AuthHandler(tornado.web.RequestHandler):
    '''
    '''
    def get(self):
        auth_code = self.get_argument('code')
        if auth_code:
            auth_uri = \
                config.wx_auth_uri % (
                    config.appid, config.appsecret,
                    auth_code,
                )
            res = mcurl.CurlHelper().get(auth_uri, resp_type='json')
            logging.info('Get userinfo: %r', res)
        else:
            self.write('授权失败，请重新授权')
