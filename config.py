# weixin config
token = 'codingmagic'
appid = 'wx163a1994e72410cd'
appsecret = '6ea461d9cfd1b7afeef9e9993b516e47'

wx_oauth_uri = ('https://open.weixin.qq.com/connect/oauth2/authorize?'
                'appid=%s&redirect_uri=%s&response_type=code'
                '&scope=%s&state=%s#wechat_redirect')
wx_auth_uri = ('https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s'
               '&secret=%s&code=%s&grant_type=authorization_code')
wx_snsapi_base = 'snsapi_base'
wx_snsapi_userinfo = 'snsapi_userinfo'
wx_redirect_uri = 'http://sun.codemagic.tk/weixin/auth'

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

MultiTextTpl = '''<xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%d</CreateTime>
                    <MsgType><![CDATA[news]]></MsgType>
                    <ArticleCount>%d</ArticleCount>
                    <Articles>
                    %s
                    </Articles>
                    </xml>'''

MultiItemTpl = '''<item>
                    <Title><![CDATA[%s]]></Title>
                    <Description><![CDATA[%s]]></Description>
                    <PicUrl><![CDATA[%s]]></PicUrl>
                    <Url><![CDATA[%s]]></Url>
                    </item>'''

# robot
tuling_robot_api = 'http://www.tuling123.com/openapi/api'
tuling_robot_key = '77dcd53ef86d9c4b2cebf35041ecbafd'
