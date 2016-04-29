# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TopicItem(scrapy.Item):
    topic = scrapy.Field()
    url = scrapy.Field()

class DetailItem(scrapy.Item):
    pass
