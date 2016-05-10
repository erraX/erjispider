# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TopicItem(scrapy.Item):
    id = scrapy.Field()
    lastUpdateTime = scrapy.Field()
    topic = scrapy.Field()
    author = scrapy.Field()
    answer = scrapy.Field()

class DetailItem(scrapy.Item):
    name = scrapy.Field()
    postedTime = scrapy.Field()
    floor = scrapy.Field()
    content = scrapy.Field()
    id = scrapy.Field()
