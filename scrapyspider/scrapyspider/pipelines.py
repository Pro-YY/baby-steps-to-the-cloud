# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import uuid
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi

import pymysql
pymysql.install_as_MySQLdb()


class ScrapyspiderPipeline:
    def process_item(self, item, spider):
        return item


class InsertDBPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self._handle_error, item, spider)
        return item

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def _conditional_insert(self, tx, item):
        raise NotImplementedError

    @staticmethod
    def _handle_error(failue, item, spider):
        print(failue)


class MyImagesPipeline(ImagesPipeline):
    store_uri = None

    def __init__(self, store_uri, download_func=None, settings=None):
        self.store_uri = store_uri
        super(MyImagesPipeline, self).__init__(store_uri, settings=settings,download_func=download_func)

    def get_media_requests(self, item, info):
        image_url = item['image_url']
        if image_url:
            yield scrapy.Request(image_url)


class InsertTsinghuaDBPipeline(InsertDBPipeline):
    def _conditional_insert(self, tx, item):
        id = str(uuid.uuid1())
        sql = "insert into tsinghua_teacher" \
              "(id, teacher_name, image_url, content)" \
              "values(%s,%s,%s,%s)"
        params = (id, item['teacher_name'], item['image_url'], item['content'])
        tx.execute(sql, params)


class InsertMicroInfoDBPipeline(InsertDBPipeline):
    def _conditional_insert(self, tx, item):
        id = str(uuid.uuid1())
        sql = "insert into microinfo" \
              "(id, company, location, company_date, level_name, tag, years_at_company, years_of_experience, " \
              "total_compensation, base, stock,bonus) " \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (id, item['company'], item['location'], item['company_date'], item['level_name'], item['tag'],
                  item['years_at_company'], item['years_of_experience'], item['total_compensation'], item['base'],
                  item['stock'], item['bonus'])
        tx.execute(sql, params)
