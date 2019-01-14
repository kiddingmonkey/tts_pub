#!/usr/bin/env python2.7 
#coding: utf-8
import time
import urllib,urllib2
import json
import sys
import io
import os
import codecs
from collections import OrderedDict
reload(sys)
sys.setdefaultencoding('utf8')
'''
1 空
2 空
3 内容
'''
"""
touser是成员ID列表（消息接收者，多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为@all，则向关注该企业应用的全部成员发送
toparty是部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
totag是标签ID列表，多个接收者用‘|’分隔。当touser为@all时忽略本参数
msgtype是消息类型，此时固定为：text
agentid是企业应用的id，整型。可在应用的设置页面查看
content是消息内容
safe表示是否是保密消息，0表示否，1表示是，默认0
"""
localtime = time.strftime('%Y.%m.%d',time.localtime(time.time()))
# baseurl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
# securl = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % access_token
class WeChatMSG(object):
    def __init__(self,content):
        self.gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        self.gettoken_content = {
                            'corpid' : 'ww4b9d1188337d061a',
                            'corpsecret' : 'cpg2MCshucNU3smZBGVlnbnc9PRkvgkdmND3uZAZSEA',
                            }
        self.main_content = {
			    "touser":"WuHao",
                            "toparty":"2|4",
                            "agentid":"1000002",
                            "msgtype": "text",
                            "text":{
                            "content":content,
                                    }
                            }
    def get_access_token(self,string):
        token_result = json.loads(string.read())
        access_token=  token_result['access_token']
        return access_token.encode('utf-8')
    def geturl(self,url,data):
        data = self.encodeurl(data)
        response = urllib2.urlopen('%s?%s' % (url,data))
        return response.read().decode('utf-8')

    def posturl(self,url,data,isjson = True):
        if isjson:
            data = json.dumps(data,ensure_ascii=False)
        response = urllib2.urlopen(url,data)
        return response.read().decode('utf-8')
    def encodeurl(self,dict):
        data = ''
        for k,v in dict.items():
            data += '%s=%s%s' % (k,v,'&')
        return data

def file_json (value_json):
    #Json = OrderedDict()
    Json = [
	      {
                "action": "talk",
                "voiceName": "Tian-Tian",
                "text": value_json
              }
           ]
    #print type(Json)
    #print Json
    #s = list(Json)
    #print s
    with codecs.open('tts.json','w','utf-8') as File:
          json.dump(Json,File)

def push_git (gitcommit):
          os.system('git add tts.json')
          os.system(gitcommit)
          os.system('git push origin master ')



if __name__ == '__main__':
    if len(sys.argv) == 4:
        touser,notuse,content = sys.argv[1:]
    else:
        print 'error segments, now exit'
        sys.exit()
    msgsender = WeChatMSG(content)
    access_token_response = msgsender.geturl(msgsender.gettoken_url, msgsender.gettoken_content)
    access_token =  json.loads(access_token_response)['access_token']
    sendmsg_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % access_token
print msgsender.posturl(sendmsg_url,msgsender.main_content)


value_json = msgsender.main_content["text"]["content"]
#print value_json
print localtime
gitcommit = 'git commit -m ' + '"' + localtime + ' tts.json 文件更新 ' + '"'
print gitcommit 

file_json(value_json)
push_git(gitcommit)

