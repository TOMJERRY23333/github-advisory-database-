# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Githubadb0Item(scrapy.Item):
    year = scrapy.Field()
    base_url = scrapy.Field()
    copy_url = scrapy.Field()


class Githubadb1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    shema_version = scrapy.Field()
    id = scrapy.Field()
    modified = scrapy.Field()
    published = scrapy.Field()
    aliases = scrapy.Field()
    summary = scrapy.Field()
    details = scrapy.Field()
    severity_score = scrapy.Field()
    severity_type = scrapy.Field()

    affected = scrapy.Field()

    references = scrapy.Field()

    cwe_ids_database_specific = scrapy.Field()
    github_reviewed_database_specific = scrapy.Field()
    severity_database_specific = scrapy.Field()


