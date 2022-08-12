# # # -*- coding: utf-8 -*-
# # # @Time  : 2022/8/6 10:11
# # # @Author: Lihaocheng
# # # @File  : test.py
#
# import requests
# import re
# from spiders.cookie import Get_Cookie
# from lxml import etree
# import csv
# import json
#
# urls = [
#     'https://login.afreecatv.com/afreeca/login.php?szFrom=adult&request_uri=https%3A%2F%2Fvod.afreecatv.com%2Fplayer%2F84552535',
#     'https://vod.afreecatv.com/player/84552535']
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
# }
# data = {
#     'username': 'JERRYHHH',
#     'password': 'HULK1176313802',
#     'action': 'login'}
# gc = Get_Cookie(urls[0], headers, data)
# gc.store_cookies()
# cookies = gc.read_cookies()
#
# URL = 'https://vod.afreecatv.com/player/84552535'
# # BASE_URL = 'https://github.com/github/advisory-database/tree/main/advisories/unreviewed/'
# # COPY_URL = 'https://raw.githubusercontent.com/github/advisory-database/main/advisories/github-reviewed/'
# # YEARS = [ i for i in range(2017,2023)]
# # ROOT_URL = BASE_URL + str(2021)
# HEADERS = {
#     # 'referer': 'https://vod.afreecatv.com/player/84553013',
#     'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47"
# }
# #
#
# response = requests.get(URL,headers=HEADERS,cookies=cookies)
#
# print(response.text)
#
# str = re.findall(r'property="og:image" content=(.*?)_r',response.text)[0]
# print(str)
#
# # with open('qq2.mp4','wb') as f:
# #     f.write(response6.content+response7.content+response.content)
#
#
# # status = response.status_code
# # tree = etree.HTML(response.text)
# #
# # string_list = tree.xpath("//a[@class='js-navigation-open Link--primary']")
# #
# # URL_L0 = BASE_URL + str(YEARS[0]) + '/' + string_list[0]
# # URL_L0_COPY = COPY_URL + str(YEARS[0]) + '/' + string_list[0]
# # # **************************************************
# #
# # response = requests.get(URL_L0,headers=HEADERS)
# # status = response.status_code
# # tree = etree.HTML(response.text)
# #
# # GHSA_list = tree.xpath("//a[@class='js-navigation-open Link--primary']/text()")
# #
# # URL_L1 = URL_L0_COPY + '/' + GHSA_list[0] + '/' + GHSA_list[0]  + '.json'
# #
# # # ********************************************************
# #
# # response = requests.get(URL_L1)
# # status = response.status_code
# # dict = json.loads(response.text)
# # print(dict)
#
# # STR = '2017-12-28T22:52:47Z'
# # import re
# #
# # str = ' '.join([i for i in re.findall(r"(.*?)T(.*?)Z",STR)[0]])
# # print(str)
# aliases  = 'CVE-2021-40663'
# if aliases:
#     alisase_list = aliases.split(',')
#     print(alisase_list)
#     for aliase in alisase_list:
#         values_aliases = (
#             aliase
#         )
#         print(values_aliases)

import os
'''
from git import Repo

# 初始化仓库
# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# empty_repo = Repo.init(os.path.join(r'E:\11763\重拾老本行\githubADB','github_advisory_db'))
# 新建远程库
# origin = empty_repo.create_remote('origin','https://github.com/github/advisory-database.git')
# origin = empty_repo.remotes[0]
# origin.fetch()
# print(empty_repo.remotes)
# print(origin.refs)

# 获取所有远程分支列表 ，返回所有链接到远程库的对象
print(repo.remotes)
# 获取远程库对象给origin 如果clone repo，则这一步已经完成
origin = repo.remotes[0]
# 获取本地heads
print(repo.heads)
# 获取所有本地分支
print(repo.refs)
# 获取远程库所有分支
print(origin.refs)
# 获取当前head指向
print(repo.head.reference)

import re

def get_commit_url(date):
    # 已有git仓库
    repo = Repo(os.path.join(r'E:\11763\ADB','advisory-database'))

    git = repo.git
    # str = git.log(pretty= r'%H',since="Tue Aug 9 19:27:01 2022 +0000").split('\n')
    # git log --pretty=format:"%H,%ad"
    commit_log_list = git.log('main',  pretty='format:"%H,%ad"',since=date,date='order').split('\n')
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    update_log = open(f'{CURRENT_DIR}\logs.txt','w')
    DATE = ''
    for commit_log in commit_log_list:
        sha1 = commit_log.split(',')[0]
        DATE = commit_log.split(',')[1]
        log = git.show(sha1)
        copy_url_list = re.findall(r"--git a/(.*?) b",log)


    update_log.write(DATE)
'''
import os
# F = open('../11.txt','w')
# F.write('DSGFD')
# F.close()

print(os.path.abspath(r'..')+'\\data')
