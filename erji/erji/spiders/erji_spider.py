# coding: utf-8

import scrapy
from erji.items import TopicItem
from scrapy.http.request import Request

# class ErjiSpider(scrapy.Spider):
#     name = "erji"
#     allowed_domains = ["www.erji.net"]
#     start_urls = [
#         "http://www.erji.net/thread.php?fid=23&search=&page=1"
#         # "http://www.erji.net/thread.php?fid=23&search=&page=2",
#         # "http://www.erji.net/thread.php?fid=23&search=&page=3"
#     ]
#
#     def parseTopics(self, response):
#         result = []
#         topicNodes = response.xpath('//tr[@class="tr3 t_one"]/td[2]/a[starts-with(@href, "read.php")]');
#
#         for topic in topicNodes:
#             title = topic.xpath('.//text()').extract_first().encode("utf8")
#             href = topic.xpath('./@href').extract_first().encode("utf8")
#             result.append([title, href])
#         return result
#
#     def parseDetail(self, response):
#         detailBox = response.xpath('//*[@id="main"]/form/div[@class="t t2"]/table/tr');
#
#         for box in detailBox:
#             name = box.xpath('//th[1]//text()').extract_first().encode("utf8");
#             print name
#
#     def parse(self, response):
#         topics = self.parseTopics(response)
#         baseUrl = "http://www.erji.net/"
#
#         for topic in topics:
#             item = TopicItem()
#             item['topic'] = topic[0]
#             item['url'] = topic[1]
#
#             request =  Request(url=baseUrl + item['url'], callback=self.parseDetail)
#             request.meta['item'] = item
#
#             yield request

class ErjiSpider(scrapy.Spider):
    name = "erji"
    allowed_domains = ["www.erji.net"]
    start_urls = [
        "http://www.erji.net/read.php?tid=1910542"
    ]

    def parseTopics(self, response):
        result = []
        topicNodes = response.xpath('//tr[@class="tr3 t_one"]/td[2]/a[starts-with(@href, "read.php")]');

        for topic in topicNodes:
            title = topic.xpath('.//text()').extract_first().encode("utf8")
            href = topic.xpath('./@href').extract_first().encode("utf8")
            result.append([title, href])
        return result

    def parse(self, response):
        baseUrl = response.url
        detailBox = response.xpath('//*[@id="main"]/form/div[@class="t t2"]/table')

        # 总共有多少页
        lastPageUrl = response.xpath('//div[@class="pages"][1]/a[last()]/@href').extract()[0]
        totalPage = lastPageUrl.split('=')[-1]

        urls = [baseUrl + '2&fpage=0&toread=&page=' + i for i in range(totalPage)]

        print urls

        for box in detailBox:
            # 楼主/层主
            name = box.xpath('./tr[1]/th[1]/b/text()').extract_first().encode('UTF8');
            postedTime = box.xpath('./tr[2]/th/div/text()').extract_first().encode('UTF8').strip()[8:-2].replace('Posted: ', '');
            floor = box.xpath('./tr[2]/th/div/span[2]/a/text()').extract_first().encode('UTF8').strip();

            # 回帖内容
            content = box.xpath('./tr[1]/th[2]/div[@class="tpc_content"]').extract_first();


            # print name, postedTime, floor

            # yield Request(url=baseUrl + , callback=self.parseDetail)
