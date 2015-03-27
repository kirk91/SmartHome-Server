# weixin info
token = 'codingmagic'
appid = 'wx163a1994e72410cd'
appsecret = '6ea461d9cfd1b7afeef9e9993b516e47'

# redis db
redis_host = '127.0.0.1'
redis_port = 6379
redis_db = 0

# response_msg tpl
TextTpl = '''<xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%d</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>'''


# robot
tuling_robot_api = 'http://www.tuling123.com/openapi/api'
tuling_robot_key = '77dcd53ef86d9c4b2cebf35041ecbafd'
