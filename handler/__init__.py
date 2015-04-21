import config

config = config

from . import index
from .weixin import wechat as weixin
from .weixin import oauth
from .device import qr
from .device import device


__all__ = ['index', 'weixin', 'oauth', 'qr', 'device']
