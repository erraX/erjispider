# coding: utf-8

import scrapy
import json
import codecs
import urlparse
import datetime
import time

from erji.items import TopicItem
from erji.items import DetailItem
from scrapy.http.request import Request

def convertDate(dateStr):
    return datetime.datetime.strptime(dateStr, '%Y-%m-%d %H:%M')

def convertTimestamp(dataStr):
    return time.mktime(convertDate(dataStr).timetuple())

def getQueryParams(url):
    '''
        解析URL的参数
        主要是要拿到帖子的id
    '''
    query = urlparse.urlparse(url).query
    return dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])

class ErjiSpider(scrapy.Spider):
    name = "erji"
    allowed_domains = ["www.erji.net"]
    totalPages = 1

    def __init__(self, *a, **kw):
        super(ErjiSpider, self).__init__(*a, **kw)
        baseUrl = "http://www.erji.net/thread.php?fid=23&search=&page=";
        # 一共要抓多少页
        self.start_urls = [baseUrl + str(i) for i in range(1, self.totalPages + 1)]

    def parseTopics(self, response):
        '''
            解析每个帖子的URL和名字
        '''
        result = []
        topicNodes = response.xpath('//tr[@class="tr3 t_one"]')
        # topicNodes = response.xpath('//tr[@class="tr3 t_one"]/td[2]/a[starts-with(@href, "read.php")]')

        for topic in topicNodes:
            titleNode = topic.xpath('./td[2]/a[starts-with(@href, "read.php")]')
            title = titleNode.xpath('.//text()').extract_first().encode("utf8")
            href = titleNode.xpath('./@href').extract_first().encode("utf8")
            lastUpdateTime = topic.xpath('./td[6]/a[starts-with(@href, "read.php")]/text()').extract_first().encode("utf8").strip()


            result.append([title, href, lastUpdateTime])
        return result

    def parseDetailPages(self, response):
        '''
            解析帖子内每一个分页
        '''
        id = response.meta['id'];
        baseUrl = response.url
        # 总共有多少页
        try:
            lastPageUrl = response.xpath('//div[@class="pages"][1]/a[last()]/@href').extract()[0]
        except:
            lastPageUrl = '=1'

        totalPages = (int)(lastPageUrl.split('=')[-1])

        pages = [baseUrl + '&fpage=0&toread=&page=' + str(i) for i in range(1, totalPages + 1)]
        # pages = [baseUrl + '&fpage=0&toread=&page=' + str(i) for i in range(1)]

        for idx, page in enumerate(pages):
            yield Request(
                    url = page,
                    meta = {
                        'pageNo': idx + 1,
                        'id': id
                    },
                    callback = self.parseDetail
                  )

    def parseDetail(self, response):
        detailBox = response.xpath('//*[@id="main"]/form/div[@class="t t2"]/table')
        id = response.meta['id']
        pageNo = response.meta['pageNo']

        for box in detailBox:
            # 帖子
            topicName = box.xpath('//*[@id="main"]/form[1]/div[1]/table/tr[1]/th/text()').extract_first()

            # 楼主/层主
            name = box.xpath('./tr[1]/th[1]/b/text()').extract_first().encode('UTF8')
            postedTime = box.xpath('./tr[2]/th/div/text()').extract_first().encode('UTF8').strip()[8:-2].replace('Posted: ', '')
            floor = box.xpath('./tr[2]/th/div/span[2]/a/text()').extract_first().encode('UTF8').strip()

            if '楼 主' in floor:
                floor = 0
            else:
                floor = floor.replace('楼', '').strip()

            # 回帖内容lastPageUrl
            content = box.xpath('./tr[1]/th[2]/div[@class="tpc_content"]').extract_first().encode('utf8')

            item = DetailItem()
            item['name'] = name
            item['postedTime'] = convertDate(postedTime)
            item['floor'] = int(floor)
            item['content'] = content
            item['id'] = id

            yield item

    def parse(self, response):
        topics = self.parseTopics(response)
        baseUrl = "http://www.erji.net/"

        for topic in topics:
            url = baseUrl + topic[1]
            id = getQueryParams(url)['tid']

            item = TopicItem()
            item['id'] = id
            item['topic'] = topic[0]
            item['lastUpdateTime'] = convertDate(topic[2])
            # item['lastUpdateTime'] = convertTimestamp(topic[2])

            # print convertDatj(topic[2])

            yield item

            yield Request(
                    url = url,
                    meta = {
                        'id': id
                    },
                    callback = self.parseDetailPages)

    def closed(self, spider):
        pass
