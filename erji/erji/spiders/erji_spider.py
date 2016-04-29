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
        "http://www.erji.net/read.php?tid=1911530"
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
        detailBox = response.xpath('//*[@id="main"]/form/div[@class="t t2"]/table');

        for box in detailBox:
            name = box.xpath('./tr[1]/th[1]/b/text()').extract_first().encode('UTF8');
            postedTime = box.xpath('./tr[2]/th/div/text()').extract_first().encode('UTF8').strip()[8:-2].replace('Posted: ', '');
