# -*- coding: utf-8 -*-
# @Time  : 2022/8/9 10:06
# @Author: Lihaocheng
# @File  : cookie.py

import requests
import json
import os

CURRENT_DIR = os.path.abspath(r'..') + '\\data'

URL = 'https://github.com/login'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/103.0.0.0 Safari/537.36 '
}
DATA = {
    'username': 'TOMJERRY23333',
    'password': 'Lhc!312457248',
    'action': 'login'}


class Get_Cookie(object):

    def __init__(self, url=URL, headers=HEADERS, data=DATA):
        self.url = url
        self.headers = headers
        self.data =data
        self.session = requests.session()

    def store_cookies(self):
        self.session.get(self.url, headers=self.headers)
        cookies_dic = requests.utils.dict_from_cookiejar(self.session.cookies)
        print('dic:',cookies_dic)
        cookies_str = json.dumps(cookies_dic)
        with open(f"{CURRENT_DIR}\cookies.txt", 'w') as f:
            f.write(cookies_str)
            f.close()

    def read_cookies(self):
        try:
            cookies_str = open(f'{CURRENT_DIR}\cookies.txt', 'r')
            cookies_dic = json.load(cookies_str)
            cookies = requests.utils.cookiejar_from_dict(cookies_dic)
            self.session.cookies = cookies
            return self.session.cookies

        except FileNotFoundError:
            self.session.post(self.url, headers=self.headers, data=self.data)


if __name__ == '__main__':

    gc = Get_Cookie()
    gc.store_cookies()
    cookies = gc.read_cookies()

    print(cookies)
