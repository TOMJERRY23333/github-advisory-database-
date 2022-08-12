# -*- coding: utf-8 -*-
# @Time  : 2022/8/11 12:33
# @Author: Lihaocheng
# @File  : update_db.py

from scrapy import Spider
from git import Repo
import json
import re
import os
from items import Githubadb1Item
import time


CURRENT_DIR = os.path.abspath(r'..') + '\\data'
COPY_URL = 'https://raw.githubusercontent.com/github/advisory-database/main/'
DEFAULT_UPDATE_TIME = "Wed Aug 10 00:08:42 2022 +0000"  # 第一次log为空，使用默认更新时间


def sync_remote(date=DEFAULT_UPDATE_TIME):
    start_urls = []
    # 已有git仓库
    repo = Repo(os.path.join(r'E:\11763\ADB', 'advisory-database'))

    git = repo.git
    # str = git.log(pretty= r'%H',since="Tue Aug 9 19:27:01 2022 +0000").split('\n')
    # git log --pretty=format:"%H,%ad"
    commit_log_list = git.log('main', '--date-order', pretty='format:"%H,%an,%ad,%s"', since=date).split('\n')
    file = open(f'{CURRENT_DIR}\log.txt', 'a')
    log_list = []

    for commit_log in commit_log_list:
        sum_dict = {}
        log_dict = {}
        commit_log = commit_log.replace('"', '')
        sha1 = commit_log.split(',')[0]
        author = commit_log.split(',')[1]
        DATE = commit_log.split(',')[2]
        desc = commit_log.split(',')[3]
        log = git.show(sha1)
        # copy_urls= ','.join(re.findall(r"--git a/(.*?) b",log))
        copy_urls = re.findall(r"--git a/(.*?) b", log)

        log_dict['commit'] = sha1
        log_dict['author'] = author
        log_dict['date'] = DATE
        log_dict['desc'] = desc
        log_dict['adv'] = copy_urls

        sum_dict['UpdateTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sum_dict['data'] = log_dict
        log_list.append(sum_dict)
        # 取url
        copy_url_list = [COPY_URL + url for url in copy_urls]
        start_urls.extend(copy_url_list)
    str_log = json.dumps(log_list, indent=2)
    file.write(str_log)
    file.close()
    return start_urls


class UpdateSpider(Spider):
    name = 'update_db'
    start_urls = []
    if not os.path.exists(os.path.join(CURRENT_DIR, 'log.txt')):
        start_urls = sync_remote()
    else:
        # 获取最新更新时间
        f1 = open(os.path.join(CURRENT_DIR, 'log.txt'), 'r')
        json1 = json.loads(f1.read())
        date1 = json1[0]['data']['date']
        f1.close()
        start_urls = sync_remote(date1)

    def parse(self, response):
        """
        解析json文件，得到items
        :param response:
        :return:
        """
        # inspect_response(response,self)
        advisories_dict = json.loads(response.text)
        item = Githubadb1Item()
        item['shema_version'] = advisories_dict["schema_version"]
        item['id'] = advisories_dict["id"]

        modify_time = advisories_dict["modified"]
        publish_time = advisories_dict["published"]
        item['modified'] = ' '.join([i for i in re.findall(r"(.*?)T(.*?)Z", modify_time)[0]])
        item['published'] = ' '.join([i for i in re.findall(r"(.*?)T(.*?)Z", publish_time)[0]])

        item['aliases'] = ','.join(advisories_dict["aliases"])

        try:
            if advisories_dict["summary"] == '':
                item['summary'] = None
            else:
                item['summary'] = advisories_dict["summary"]
        except Exception as e:
            self.logger.info('%s出错', e)
            item['summary'] = None

        item['details'] = advisories_dict['details'].strip().replace('#', '').replace('\n', '')

        if not advisories_dict["severity"]:
            item['severity_score'] = None
            item['severity_type'] = None
        else:
            item['severity_score'] = advisories_dict["severity"][0]['score']
            item['severity_type'] = advisories_dict["severity"][0]['type']

        # *************** 解析 affected **************
        if not advisories_dict["affected"]:
            item['affected'] = None
        else:
            item['affected'] = json.dumps(advisories_dict["affected"], indent=2)

        # ************** 解析 references ************
        item['references'] = json.dumps(advisories_dict["references"], indent=2)

        if advisories_dict["database_specific"] is None:
            item['cwe_ids_database_specific'] = None
            item['github_reviewed_database_specific'] = None
            item['severity_database_specific'] = None
        else:
            item['cwe_ids_database_specific'] = ','.join(advisories_dict["database_specific"]['cwe_ids'])
            item['github_reviewed_database_specific'] = advisories_dict["database_specific"]['github_reviewed']
            item['severity_database_specific'] = advisories_dict["database_specific"]['severity']

        yield item

    # if __name__ == '__main__':
    #     get_commit_url('Tue Aug 9 19:27:01 2022 +0000')
    #     f1 = open('log.txt','r')
    #     json1 = json.loads(f1.read())
    #     date = json1[0]['date']
    #     url = json1[0]['adv']
    #     print(date)
    #     print(url)

# path = r"E:\11763\ADB\advisory-database\advisories\unreviewed\2022\05"
# file_name_list = os.listdir(path)
# print(file_name_list[0],file_name_list[-1])
