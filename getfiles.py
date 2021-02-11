#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/10/30 8:52:03

import io
import sys
import time
import unicodedata
import requests
 
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

def getData(url, num_retries=2, user_agent='jenny', proxies=None, data_type='pdf'):
    '''下载一个指定的URL并返回网页内容
        参数：
            url(str): URL
        关键字参数：
            user_agent(str):用户代理（默认值：wswp）
            proxies（dict）： 代理（字典）: 键：‘http’'https'
            值：字符串（‘http(s)://IP’）
            num_retries(int):如果有5xx错误就重试（默认：2）
            #5xx服务器错误，表示服务器无法完成明显有效的请求。
            #https://zh.wikipedia.org/wiki/HTTP%E7%8A%B6%E6%80%81%E7%A0%81
    '''
    print('==========================================')
    print('Downloading:', url)
    headers = {'User-Agent': user_agent} #头部设置，默认头部有时候会被网页反扒而出错
    try:
        resp = requests.get(url, headers=headers, proxies=proxies, verify=False) #简单粗暴，.get(url)
        if data_type == 'html' or data_type == 'txt':
            _data = resp.text #获取网页内容，字符串形式
        elif data_type == 'json':
            _data = resp.json()
        elif data_type == 'img' or data_type == 'pdf':
            _data = resp.content
        else:
            raise ValueError('Unknown response data type')
        if resp.status_code >= 400: #异常处理，4xx客户端错误 返回None
            print('Download error:', resp.text)
            html = None
            if num_retries and 500 <= resp.status_code < 600:
                # 5类错误
                return download(url, num_retries - 1)#如果有服务器错误就重试两次

    except requests.exceptions.RequestException as e: #其他错误，正常报错
        print('Download error:', e)
        _data = None
    return _data 
 
def saveFile(file_name, file_content, file_type='pdf'):  
#    注意windows文件命名的禁用符，比如 /  
    if file_type=='pdf' or file_type =='img':
        with open (file_name , "wb") as f:
            f.write( file_content )  
    elif file_type=='txt' or file_type=='html' or file_type=='json':
        with open (file_name , "w", encoding ='utf-8-sig') as f:
            f.write( file_content )  

		
