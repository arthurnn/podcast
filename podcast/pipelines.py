# Define your item pipelines here
from scrapy import log
from twisted.enterprise import adbapi

import time
import MySQLdb.cursors

class MySQLStorePipeline(object):

    def __init__(self):
        # @@@ hardcoded db settings
        # TODO: make settings configurable through settings
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db='podcastdb',
                user='root',
                passwd='root',
                cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8',
                use_unicode=True
            )

    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

        return item

    def _conditional_insert(self, tx, item):
        # create record if doesn't exist. 
        # all this block run on it's own thread
        tx.execute("select * from item where website = %s", (item['website'], ))
        result = tx.fetchone()
        if result:
            log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
        else:
            tx.execute(\
                "insert into item (title, website, author, price, category, lang, email, created) "
                "values (%s, %s, %s, %s, %s, %s, %s, %s)",
                (item['title'],
                 item['website'],
                 item['author'],
                 item['price'],
                 item['category'],
                 item['lang'],
                 item['email'],
                 time.time())
            )
            log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)

