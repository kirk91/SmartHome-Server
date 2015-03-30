#! /usr/bin/env python
# coding: utf-8

try:
    from xml.etree import cElementTree as ET
except:
    from xml.etree import ElementInclude as ET

xml_str = '''<xml><ToUserName><![CDATA[gh_318d9893f46d]]></ToUserName>
    <FromUserName><![CDATA[oiSYOt4KRhKE_xQXa-OuATGGRUMg]]></FromUserName>
    <CreateTime>1427691945</CreateTime>
    <MsgType><![CDATA[event]]></MsgType>
    <Event><![CDATA[scancode_waitmsg]]></Event>
    <EventKey><![CDATA[scancode_waitmsg]]></EventKey>
    <ScanCodeInfo><ScanType><![CDATA[qrcode]]></ScanType>
    <ScanResult><![CDATA[http://weixin.qq.com/q/PUwbhT-mkYnoPI06FmBN]]></ScanResult>
    </ScanCodeInfo>
    </xml>'''


def parse_request_xml(xml_str):
        msg = dict()
        root = ET.fromstring(xml_str)
        if root.tag == 'xml':
            for child in root:
                if child.getchildren():
                    child.text = dict()
                    for subchild in child:
                        child.text[subchild.tag] = subchild.text
                msg[child.tag] = child.text
        return msg


if __name__ == '__main__':
    print parse_request_xml(xml_str)

