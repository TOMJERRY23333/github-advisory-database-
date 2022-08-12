# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import json


class GithubadbPipeline(object):

    def open_spider(self, spider):
        """
        该方法用于创建数据库连接池对象并连接数据库
        :param spider:
        :return:
        """
        db = spider.settings.get('MYSQL_DA_NAME', 'github_advisory_db')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', '123456')

        self.db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        """
        此方法用于数据插入和关闭数据库
        :param spider:
        :return:
        """
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):
        """
        调用数据输入函数inser_db()
        :param item: 数据
        :param spider:
        :return:
        """
        self.insert_db(item)

        return item

    def insert_db(self, item):
        """
        语句构造方法
        :param item:
        :return:
        """
        values_all = (
            item['shema_version'],
            item['id'],
            item['modified'],
            item['published'],
            item['aliases'],
            item['summary'],
            item['details'],
            item['severity_type'],
            item['severity_score'],
            item['affected'],
            item['references'],
            item['cwe_ids_database_specific'],
            item['severity_database_specific'],
            item['github_reviewed_database_specific']
        )
        sql_all = "REPLACE INTO adv_all (shema_version, id, modified, published, aliases , summary , details , severity_type, severity_score, affected, reference, cwe_ids_database_specific, severity_database_specific, github_reviewed_database_specific) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.db_cur.execute(sql_all, values_all)

        # aliases表中aliase为主键
        if item['aliases']:
            alisase_list = item['aliases'].split(',')
            for aliase in alisase_list:
                values_aliases = (
                    aliase,
                    item['id']
                )
                sql_aliases = "REPLACE INTO aliases(aliase, id) VALUES(%s,%s)"
                self.db_cur.execute(sql_aliases, values_aliases)
        # else:
        #     values_aliases = (
        #         item['aliases'],
        #         item['id']
        #
        #     )
        #     sql_aliases = "INSERT INTO aliases(aliase, id ) VALUES(%s,%s)"
        #     self.db_cur.execute(sql_aliases, values_aliases)

        # affected表
        if item['affected']:
            affected_list = json.loads(item['affected'])
            for affected_dict in affected_list:
                try:
                    affected_package_ecosystem = affected_dict['package']['ecosystem']
                except:
                    affected_package_ecosystem = None
                try:
                    affected_package_name = affected_dict['package']['name']
                except:
                    affected_package_name = None
                try:
                    database_specific = json.dumps(affected_dict['database_specific'],indent=2)
                except:
                    database_specific = None

                try:
                    for affected_ranges in affected_dict['ranges']:
                        try:
                            affected_ranges_type = affected_ranges['type']
                        except:
                            affected_ranges_type = None
                        try:
                            affected_ranges_events_intro = affected_ranges['events'][0]['introduced']
                        except:
                            affected_ranges_events_intro = None
                        try:
                            affected_ranges_events_fixed = affected_ranges['events'][1]['fixed']
                        except:
                            affected_ranges_events_fixed = None

                        values_affected = (
                            item['id'],
                            affected_package_ecosystem,
                            affected_package_name,
                            affected_ranges_type,
                            affected_ranges_events_intro,
                            affected_ranges_events_fixed,
                            database_specific
                        )
                        sql_affected = "REPLACE INTO affected(id, affected_package_ecosystem, affected_package_name, affected_ranges_type, affected_ranges_events_intro, affected_ranges_events_fixed,database_specific) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                        self.db_cur.execute(sql_affected, values_affected)
                except:
                    affected_ranges_type = None
                    affected_ranges_events_intro = None
                    affected_ranges_events_fixed = None
                    values_affected = (
                        item['id'],
                        affected_package_ecosystem,
                        affected_package_name,
                        affected_ranges_type,
                        affected_ranges_events_intro,
                        affected_ranges_events_fixed,
                        database_specific
                    )
                    sql_affected = "REPLACE INTO affected(id, affected_package_ecosystem, affected_package_name, affected_ranges_type, affected_ranges_events_intro, affected_ranges_events_fixed,database_specific) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                    self.db_cur.execute(sql_affected, values_affected)
        else:
            affected_package_ecosystem = None
            affected_package_name = None
            affected_ranges_type = None
            affected_ranges_events_intro = None
            affected_ranges_events_fixed = None
            database_specific = None
            values_affected = (
                item['id'],
                affected_package_ecosystem,
                affected_package_name,
                affected_ranges_type,
                affected_ranges_events_intro,
                affected_ranges_events_fixed,
                database_specific
            )
            sql_affected = "REPLACE INTO affected(id, affected_package_ecosystem, affected_package_name, affected_ranges_type, affected_ranges_events_intro, affected_ranges_events_fixed,database_specific) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            self.db_cur.execute(sql_affected, values_affected)

        # refer表
        refer_json = json.loads(item['references'])
        for refer_dict in refer_json:
            refer_type = refer_dict['type']
            refer_url = refer_dict['url']
            values_references = (
                item['id'],
                refer_type,
                refer_url
            )
            sql_references = "REPLACE INTO refers(id, refer_type, refer_url) VALUES(%s,%s,%s)"
            self.db_cur.execute(sql_references, values_references)
