# coding: utf-8

import scrapy
import json
import codecs

from erji.items import TopicItem
from erji.items import DetailItem
from scrapy.http.request import Request

f = codecs.open('output.txt', 'w', 'utf8')

class ErjiSpider(scrapy.Spider):
    erjiData = {}
    name = "erji"
    allowed_domains = ["www.erji.net"]

    start_urls = [
        "http://www.erji.net/thread.php?fid=23&search=&page=1"
        # "http://www.erji.net/thread.php?fid=23&search=&page=2",
        # "http://www.erji.net/thread.php?fid=23&search=&page=3"
    ]

    def parseTopics(self, response):
        result = []
        topicNodes = response.xpath('//tr[@class="tr3 t_one"]/td[2]/a[starts-with(@href, "read.php")]')

        for topic in topicNodes:
            title = topic.xpath('.//text()').extract_first().encode("utf8")
            href = topic.xpath('./@href').extract_first().encode("utf8")
            result.append([title, href])
        return result

    def parseDetailPages(self, response):
        # print 'erjiData', self.erjiData
        url = response.meta['url'];
        baseUrl = response.url
        # 总共有多少页
        try:
            lastPageUrl = response.xpath('//div[@class="pages"][1]/a[last()]/@href').extract()[0]
        except:
            lastPageUrl = '=1'

        totalPage = (int)(lastPageUrl.split('=')[-1])

        # pages = [baseUrl + '&fpage=0&toread=&page=' + str(i) for i in range(1, totalPage + 1)]
        pages = [baseUrl + '&fpage=0&toread=&page=' + str(i) for i in range(1)]

        for idx, page in enumerate(pages):
            yield Request(
                    url=page,
                    meta = {
                        'pageNo': idx+1,
                        'url': url
                    },
                    callback=self.parseDetail
                  )

        # self.erjiData['url'] = {}
        # self.erjiData['url']['pageInfo'] = pageList


    def parseDetail(self, response):
        detailBox = response.xpath('//*[@id="main"]/form/div[@class="t t2"]/table')
        pageNo = response.meta['pageNo']
        url = response.meta['url']

        for box in detailBox:
            # 帖子
            topicName = box.xpath('//*[@id="main"]/form[1]/div[1]/table/tr[1]/th/text()').extract_first()

            # 楼主/层主
            name = box.xpath('./tr[1]/th[1]/b/text()').extract_first().encode('UTF8')
            postedTime = box.xpath('./tr[2]/th/div/text()').extract_first().encode('UTF8').strip()[8:-2].replace('Posted: ', '')
            floor = box.xpath('./tr[2]/th/div/span[2]/a/text()').extract_first().encode('UTF8').strip()

            # 回帖内容lastPageUrl
            content = box.xpath('./tr[1]/th[2]/div[@class="tpc_content"]').extract_first().encode('utf8')

            item = DetailItem()
            item['name'] = name
            item['postedTime'] = postedTime
            item['floor'] = floor
            item['content'] = content

            # pageList.append(item)

            self.erjiData[url]['pages'].append(item)

            # yield item

        # return pageList

        # print 'PPPPPPPPPPAGE', pageList, pageNo, url
            # print name, postedTime, floor
            # yield item
         
    def parse(self, response):
        topics = self.parseTopics(response)
        baseUrl = "http://www.erji.net/"

        for topic in topics:
            url = topic[1]

            self.erjiData[baseUrl + url] = {}
            self.erjiData[baseUrl + url]['title'] = topic[0]
            self.erjiData[baseUrl + url]['pages'] = []

            yield Request(
                    url = baseUrl + url,
                    meta = {
                        'url': baseUrl + url
                    },
                    callback = self.parseDetailPages)

    def closed(self, spider):
        print >> f, self.erjiData
        # jsonStr = json.dumps(self.erjiData, ensure_ascii=False)
        # print jsonStr
        # print self.erjiData
