#!/usr/bin/python
# coding=utf-8

import scrapy
from autohome_spider.items import SeriesItem


# 车系数据爬虫
class SeriesSpider(scrapy.Spider):
    name = 'series'
    allowed_domains = 'autohome.com.cn'
    # start_urls = ['http://www.autohome.com.cn/grade/carhtml/A.html']
    start_urls = [
        'http://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i)
        for i in range(26)
    ]

    def parse(self, response):
        for brandPart in response.xpath('body/dl'):
            brand_id = brandPart.xpath('@id')[0].extract()
            # print 'brandID[%s].' % (brand_id)
            # make_name = brandPart.xpath('dd/div/a/text()')[0].extract()

            n = brandPart.xpath('dd/div[@class="h3-tit"]').extract()
            print "-------- %d" % len(n)
            for i in range(len(n)):
                # print i
                s = 'dd/div[@class="h3-tit"][%d]/a/text()' % (i+1)
                make_name = brandPart.xpath(s)[0].extract()
                # print make_name

                # print 'brandID[%s], makeName[%s].' % (brand_id, make_name)

                # print 'brandID[%s], makeName[%s], series[%s].' % (brand_id, make_name, seriesParts)
                seriesParts = brandPart.xpath(
                    'dd/ul[@class="rank-list-ul"][%d]/li' % (i+1))
                for seriesPart in seriesParts:
                    series = SeriesItem()
                    try:
                        # name = seriesPart.xpath(
                        #     'h4/a/text()')[0].extract()
                        # print name

                        series['brand_id'] = brand_id
                        series['make_name'] = make_name
                        series['id'] = seriesPart.xpath('@id')[0].extract()
                        series['name'] = seriesPart.xpath(
                            'h4/a/text()')[0].extract()
                        series['price'] = seriesPart.xpath(
                            'div/a/text()')[0].extract()
                        series['url'] = seriesPart.xpath(
                            'h4/a/@href')[0].extract()
                        # series['url'] = seriesPart.xpath('h4/a/@href')[0].re(r'(//www\.autohome\.com\.cn/\d+)')
                        # serie_url = 'http:' + series['url']
                        # request = scrapy.Request(
                        #     url=serie_url, callback=self.parse_model_selling, dont_filter=True)
                        # request.meta['series_id'] = series['id']
                        # yield request

                        yield series
                    except:
                        pass

    def parse_model_selling(self, response):
        print response.xpath(
            '//div[@class="spec-wrap active"]/dl[1]/dd[1]/div/div/p[1]/a/text()').extract()
