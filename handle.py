#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2021/2/9 21:33:50

import hashlib
import requests
import json
import reply
import receive
import web
import getfiles as gf
import urls
import get_token as gt
from requests_toolbelt import MultipartEncoder
import makepoem
import ocr

class Handle(object):

    ''' Initialise the configuration with the token
    def GET(self):
        print('now listening...')
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "1q2w3e4r5t" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            #map(sha1.update, list)
            sha1.update(list[0].encode('utf-8'))
            sha1.update(list[1].encode('utf-8'))
            sha1.update(list[2].encode('utf-8'))
            hashcode = sha1.hexdigest()
            print ("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                print('signature wrong')
                return ""
        except Exception as Argument:
            print('something wrong')
            return Argument
    '''
    def POST(self):
        
    
        def get_id(img):

            _token = gt.get_token()
            _url = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token=' + _token + '&type=image'
            print('url=', _url)

            payload = {
                    'file':('upload.jpg', img, 'image/jpg')
                    }
            m = MultipartEncoder(payload)
            headers = {
                    'Content-Type':m.content_type,
                    'other-keys':'other-values'
                    }
            _id = requests.post(_url, headers=headers, data=m).json()
            print('post request returns:', _id)
            _id = _id['media_id']
            print(_id)
            return _id

        #try:
        webData = web.data()
        print ("Handle Post webdata is ", webData)
        #后台打日志
        recMsg = receive.parse_xml(webData)
        #print(recMsg.Content.decode('utf-8'))
        _data = ''
        if isinstance(recMsg, receive.Msg): 
            #print(urls.triggers)
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            if recMsg.MsgType == 'text':
                for trigger in urls.triggers:
                    if trigger in recMsg.Content.decode('utf-8'):
                        print('got the keyword:', trigger)
                    
                        for key, item in urls.URL.items():
                            if item['trigger']==trigger:
                                _item = item
                                break
                        if _item['type']=='txt_event':
                            print('now making poem...')
                            _data = _item['keyword']()
                            print(_data)
                            replyMsg = reply.TextMsg(toUser, fromUser, _data)
                            return replyMsg.send()
                        else:
                            _data = gf.getData(_item['url'], data_type=_item['type'])
                        if _data:
                            if _item['type']=='txt' or _item['type']=='json':
                                if _item['type']=='json':
                                    _data = _data[_item['keyword']]
                                replyMsg = reply.TextMsg(toUser, fromUser, _data)
                            elif _item['type']=='img':
                                _id = get_id(_data)
                                replyMsg = reply.ImageMsg(toUser, fromUser, _id)

                            return replyMsg.send()
                        else:
                            print('request data failed')
                            _data = ''

                        break
                else:
                    _data = urls.DEFAULT_MSG
                    replyMsg = reply.TextMsg(toUser, fromUser, _data)
                    return replyMsg.send()

            elif recMsg.MsgType == 'image':
                
                _url = recMsg.PicUrl
                _data = gf.getData(_url, data_type='img')
                _data = ocr.Ocr(_data)
                _id = get_id(_data)
                replyMsg = reply.ImageMsg(toUser, fromUser, _id)
                return replyMsg.send()

            
        if _data =='':
            print ("暂且不处理")
            return "success"
        #except Exception as Argment:
        #    print('something wrong happened', Argment)
        #    return Argment
