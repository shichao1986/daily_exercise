# -*- coding: utf-8 -*-
"""
时间: 2019/6/6 11:31

作者: shichao

更改记录:

重要说明:
"""

import urllib.request
import urllib.parse
import ssl
from bs4 import BeautifulSoup

context = ssl._create_unverified_context()


cookies = {}

def update_cookies(cks):
    cks_set = cks.split(';')
    length = len(cks_set)
    key = ''
    for i in range(0, length):
        try:
            cks_set[i].strip()
            k = cks_set[i].split('=')[0]
            v = cks_set[i].split('=')[1]
            if i == 0:
                key = k
                cookies[key] = {'value':v}
            else:
                cookies[key][k] = v
        except Exception as e:
            print(e)
            print('ignore cookie attr:{}'.format(cks_set[i]))

def get_cookies():
    cl = []
    for item in cookies:
        s = '='.join([item,cookies[item]['value']])
        cl.append(s)

    return '; '.join(cl)

# values = {}
# values['username'] = 'username'
# values['password'] = 'password'
# #geturl = url + '?' + values


if __name__ == '__main__':
    url = "https://iot.cyai.com/web/login/"

    import pdb;
    pdb.set_trace()

    with urllib.request.urlopen(url, context=context) as response:
        html = response.read().decode()

    bs = BeautifulSoup(html, features="html.parser")
    target_input = bs.find(name='input', attrs={'name': 'csrfmiddlewaretoken'})
    csrfmiddlewaretoken = target_input.get('value')

    get_setcookies = response.headers['Set-Cookie']

    if isinstance(get_setcookies, str):
        update_cookies(get_setcookies)

    pass_data = {
        'csrfmiddlewaretoken':csrfmiddlewaretoken,
        'next':'None',
        'username':'release_admin',
        'password':'password'
    }

    data = urllib.parse.urlencode(pass_data).encode('ascii')

    req = urllib.request.Request(url, data=data, method='POST', headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Content-Length':len(data),
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie': get_cookies(),
        'Host': 'iot.cyai.com',
        'Origin': 'https://iot.cyai.com',
        'Pragma': 'no-cache',
        'Referer': 'https://iot.cyai.com/web/login/',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    })

    with  urllib.request.urlopen(req, context=context) as response:
        html = response.read()

    print('response:{}'.format(dir(response)))  # 200是正常响应


