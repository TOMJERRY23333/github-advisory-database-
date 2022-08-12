# -*- coding: utf-8 -*-
# @Time  : 2022/8/11 21:07
# @Author: Lihaocheng
# @File  : reset.py

from scrapy import Spider,Request
import json
import re
import os
from items import Githubadb1Item


class ResetSpider(Spider):
    name = 'reset_db'
    start_urls = ['https://github.com']

    def parse(self,response):
        ROOT_PATH = r"E:\11763\ADB\advisory-database\advisories"
        COPY_URL = 'https://raw.githubusercontent.com/github/advisory-database/main/advisories/{mode}/'
        file_name_list0 = os.listdir(ROOT_PATH)
        for review in file_name_list0:
            COPY_URL1 = COPY_URL.format(mode=review)
            ROOT_PATH1 = ROOT_PATH + "\\" + review
            file_name_list1 = os.listdir(ROOT_PATH1)
            for year in file_name_list1:
                COPY_URL2 = COPY_URL1 + year + '/'
                ROOT_PATH2 = ROOT_PATH1 + '\\' + year
                file_name_list2 = os.listdir(ROOT_PATH2)
                for month in file_name_list2:
                    COPY_URL3 = COPY_URL2 + month + '/'
                    if 'GHSA' in month:
                        ghsa = re.findall(r'[A-Za-z0-9_\-\u4e00-\u9fa5]+',month)[1]
                        COPY_URL4 = COPY_URL3  + ghsa + '.json'
                        # self.start_urls.append(COPY_URL)
                        yield Request(COPY_URL4, callback=self.parse_json)
                    else:
                        ROOT_PATH3 = ROOT_PATH2 + '\\' + month
                        file_name_list3 = os.listdir(ROOT_PATH3)
                        for ghsa in file_name_list3:
                            COPY_URL4 = COPY_URL3 + ghsa + '/' + ghsa + '.json'
                            # self.start_urls.append(COPY_URL)
                            yield Request(COPY_URL4, callback=self.parse_json)

    def parse_json(self, response):
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