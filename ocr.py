#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2020/5/28 15:04:50

import sys
import json
from io import StringIO, BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont

'''
Baidu-AI based OCR
'''

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
#from urllib.parse import quote_plus

# 防止https证书校验不正确
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = ''
SECRET_KEY = ''

OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"
"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


"""
    获取token
"""
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    result_str = result_str.decode()


    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

"""
    读取文件
"""
def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()


"""
    调用远程服务
"""
def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)

'''
enchance the picture to raise the correct-rate of OCR 
'''
# 二值处理
# 设定阈值threshold，像素值小于阈值，取值0，像素值大于阈值，取值1
# 阈值具体多少需要多次尝试，不同阈值效果不一样
def get_table(threshold=115):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


def expression_parser(word_string):

    '''
    WIP: expression-parser
    '''

    if '=' in word_string and word_string[0]!= '=' and word_string[-1]!='=':
        equal_pos = word_string.find('=')
        if word_string[equal_pos+1:].isdigit():
            _result = int(word_string[equal_pos+1:])
            exp_str = word_string[:equal_pos]
            exp_str = exp_str.replace('÷', '/')
            exp_str = exp_str.replace('×', '*')

            try:
                if eval(exp_str) == _result:
                    return 'Right'
                else:
                    return 'Wrong'
            except Exception as error:
                print(word_string[:equal_pos] + ' seems strange...')
                return 'Uncertain'
        else:
            return 'Uncertain'
    else:
        return 'Uncertain'
    

def Ocr(im):

    # 将原始图片灰度化
    grey_im = Image.open(BytesIO(im)).convert('L')
    # 保存灰度化图片
    #grey_im.save('grey.png')

    # 打开灰度化图片并进行二值处理
    #binary_im = Image.open('grey.png').point(get_table(95), "1")
    binary_im = grey_im.point(get_table(95), "1")
    # 保存二值化图片

    file_name = 'binary.jpg'
    binary_im.save(file_name, 'jpeg')



    # 获取access token
    token = fetch_token()
    # 拼接通用文字识别高精度url
    image_url = OCR_URL + "?access_token=" + token

    text = ""
    # 读取书籍页面图片
    file_content = read_file(file_name)

    para = {'image': base64.b64encode(file_content), 
            'recognize_granularity': 'small', 
            'words_type': 'handprint_mix'
            }

    # 调用文字识别服务
    result = request(image_url, urlencode(para))

    # 解析返回结果
    _image = Image.open(BytesIO(im)) #Image.open(original_file)
    draw = ImageDraw.Draw(_image)

    result_json = json.loads(result)
    text_font = ImageFont.truetype('STXIHEI.TTF', 50)
    for words_result in result_json["words_result"]:
        #print(words_result)
        print(words_result['words'])
        location = words_result['location']
        rect = (location['left'], location['top'], 
                location['left'] + location['width'], 
                location['top'] + location['height'])
        draw.rectangle(rect, None, 'red')
        exp_result = expression_parser(words_result['words'])
        if exp_result == 'Right':
            draw.text((location['left'] + location['width'] + 10, 
                location['top'] + 5), '正确', (0,200,0), font=text_font) 
        elif exp_result == 'Wrong':
            draw.text((location['left'] + location['width'] + 10, 
                location['top'] + 5), '错误', (200,0,0), font=text_font) 

    imgByteArr = BytesIO()
    _image.save(imgByteArr, format='JPEG')
    return imgByteArr.getvalue() #.save('result.jpg', 'jpeg')



if __name__ == '__main__':

    # 打开原始图片
    original_file = '2.jpg'
    im = Image.open(original_file)

    _image = Ocr(im)
    _image.save('result.jpg', 'jpeg')

