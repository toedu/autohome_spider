#!/usr/bin/python
# coding=utf-8

import scrapy
from autohome_spider.items import SeriesItem


# 车系数据爬虫
class SeriesSpider(scrapy.Spider):
    name = 'model'
    allowed_domains = 'autohome.com.cn'
    start_urls = ['http://www.autohome.com.cn/grade/carhtml/A.html']
    # start_urls = [
    #     'http://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i)
    #     for i in range(26)
    # ]

    def parse(self, response):
        # 循环品牌
        for brandPart in response.xpath('body/dl'):
            brand_id = brandPart.xpath('@id')[0].extract()
            # 循环厂商
            n = brandPart.xpath('dd/div[@class="h3-tit"]').extract()
            for i in range(len(n)):

                # s = 'dd/div[@class="h3-tit"][%d]/a/text()' % (i+1)
                # 厂商名称
                # make_name = brandPart.xpath(s)[0].extract()

                # 循环车系
                seriesParts = brandPart.xpath(
                    'dd/ul[@class="rank-list-ul"][%d]/li' % (i+1))
                for seriesPart in seriesParts:
                    try:
                        price = seriesPart.xpath('div/a/text()')[0].extract()
                        if price == "暂无":
                            continue

                        series_id = seriesPart.xpath('@id')[0].extract()
                        url = 'http:' + \
                            seriesPart.xpath('h4/a/@href')[0].extract()

                        request = scrapy.Request(
                            url=url, callback=self.parse_model_selling, dont_filter=True)
                        request.meta['brand_id'] = brand_id
                        request.meta['series_id'] = series_id
                        yield request
                    except:
                        pass

    def parse_model_selling(self, response):
        brand_id = response.meta['brand_id']
        series_id = response.meta['series_id']
        # 循环发动机类型
        for enginePart in response.xpath('//div[@class="spec-wrap active"]/dl'):
            engine_type = enginePart.xpath(
                'dt/div[1]/span/text()')[0].extract()
            print "%s, %s, %s" % (brand_id, series_id, engine_type)
            # 循环车型
            for seriesPart in enginePart.xpath('dd'):
                series_name = seriesPart.xpath(
                    'div[1]/div/p[1]/a/text()')[0].extract()
                series_price = seriesPart.xpath(
                    'div[3]/p/span/text()')[0].extract()
                print "------------ %s, %s" % (series_name, series_price)
                # print "----------------"

        # print response.xpath(
        #     '//div[@class="spec-wrap active"]/dl[1]/dd[1]/div/div/p[1]/a/text()').extract()
