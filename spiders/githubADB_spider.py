# -*- coding: utf-8 -*-
# @Time  : 2022/8/6 10:10
# @Author: Lihaocheng
# @File  : githubADB_spider.py

from scrapy.http import Request
from scrapy import Spider
from scrapy.shell import inspect_response
from items import Githubadb0Item
from items import Githubadb1Item
from spiders.cookie import Get_Cookie
import re
import json


class ADBSpider(Spider):
    name = 'githubADB'
    INDEX = "//a[@class='js-navigation-open Link--primary']/text()"
    gc = Get_Cookie()
    # gc.store_cookies()
    COOKIE = gc.read_cookies()
    HEADERS = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77",
    }

    def start_requests(self):
        """
        :return: 可迭代的request对象
        """
        BASE_URL = 'https://github.com/github/advisory-database/tree/main/advisories/{mode}/'
        COPY_URL = 'https://raw.githubusercontent.com/github/advisory-database/main/advisories/{mode}/'

        item0 = Githubadb0Item()
        item1 = Githubadb0Item()

        item0['base_url'] = BASE_URL.format(mode='github-reviewed')
        item0['copy_url'] = COPY_URL.format(mode='github-reviewed')

        item1['base_url'] = BASE_URL.format(mode='unreviewed')
        item1['copy_url'] = COPY_URL.format(mode='unreviewed')
        self.logger.info('BASE_URL: %s', item0['base_url'])
        return [Request(item0['base_url'], callback=self.parse_years,
                        headers=self.HEADERS,cookies= self.COOKIE, meta={'item': item0}),
                Request(item1['base_url'], callback=self.parse_years,
                        headers=self.HEADERS,cookies= self.COOKIE, meta={'item': item1})]

    def parse_years(self, response):
        """
        解析发布年
        :param response:
        :return:
        """
        BASE_URL = response.meta['item']['base_url']
        COPY_URL = response.meta['item']['copy_url']
        years_list = response.xpath(self.INDEX).extract()
        for year in years_list:
            item0 = Githubadb0Item()
            item0['year'] = str(year)
            item0['base_url'] = BASE_URL
            item0['copy_url'] = COPY_URL
            root_url = BASE_URL + str(year)
            self.logger.info('root_url: %s', root_url)
            yield Request(root_url, callback=self.parse, headers=self.HEADERS,cookies= self.COOKIE, meta={'item': item0})

    def parse(self, response):
        """
        解析每个发布年下的月份文件夹/json文件
        :param response:
        :return:
        """
        year = response.meta['item']['year']
        BASE_URL = response.meta['item']['base_url']
        COPY_URL = response.meta['item']['copy_url']
        month_list = response.xpath("//a[@class='js-navigation-open Link--primary']")
        for month in month_list:
            month0 = month.xpath('text()').extract()[0]
            if "GHSA" in month0:
                # 判断含GHSA，得到月份
                month = month.xpath('./span/text()').extract()[0]  # 获得 ”月份/“
                url_l0 = COPY_URL + year + '/' + month + month0 + '/' + month0 + '.json'
                yield Request(url_l0, callback=self.parse_json)
            else:
                item0 = Githubadb0Item()
                item0['copy_url'] = COPY_URL + year + '/' + month0 + '/'
                url_l0 = BASE_URL + year + '/' + month0
                yield Request(url_l0, callback=self.parse_further,
                              headers=self.HEADERS,cookies= self.COOKIE, meta={'item': item0})

    def parse_further(self, response):
        """
        解析得到漏洞信息的GHSA
        :param response:
        :return:
        """
        COPY_URL = response.meta['item']['copy_url']
        ghsa_list = response.xpath(self.INDEX).extract()
        for ghsa in ghsa_list:
            url_l1 = COPY_URL + ghsa + '/' + ghsa + '.json'
            yield Request(url_l1, callback=self.parse_json)

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
