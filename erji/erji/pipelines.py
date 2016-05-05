# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from pymongo import MongoClient

from erji.items import TopicItem
from erji.items import DetailItem

class ErjiPipeline(object):
    def __init__(self):
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.topicCollection = db['topic']
        self.detailCollection = db['detail']

    def process_item(self, item, spider):
        if isinstance(item, TopicItem):
            self.store_topic(dict(item))
        elif isinstance(item, DetailItem):
            self.store_detail(dict(item))

        return item

    def store_topic(self, item):
        id = item["id"]
        self.topicCollection.update_one({"id": id}, {"$set": item}, True)

    def store_detail(self, item):
        id = item["id"]
        floor = item["floor"]
        self.detailCollection.update_one({"id": id, "floor": floor}, {"$set": item}, True)
