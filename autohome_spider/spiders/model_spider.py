#!/usr/bin/python
# coding=utf-8

import scrapy
from autohome_spider.items import ModelItem


# 车系数据爬虫
class SeriesSpider(scrapy.Spider):
    name = 'model'
    allowed_domains = 'autohome.com.cn'
    start_urls = ['http://www.autohome.com.cn/grade/carhtml/A.html']
    # start_urls = [
    #     'http://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i)
    #     for i in range(26)
    # ]

    request_ids = [35, 34]

    def parse(self, response):
        # 循环品牌
        for brandPart in response.xpath('body/dl'):
            brand_id = brandPart.xpath('@id')[0].extract()
            # 循环厂商
            n = brandPart.xpath('dd/div[@class="h3-tit"]').extract()
            for i in range(len(n)):
                # 循环车系
                seriesParts = brandPart.xpath(
                    'dd/ul[@class="rank-list-ul"][%d]/li' % (i+1))
                for seriesPart in seriesParts:
                    try:
                        # 过滤无价格的车系
                        price = seriesPart.xpath('div/a/text()')[0].extract()
                        if price == "暂无":
                            continue

                        series_id = seriesPart.xpath('@id')[0].extract()
                        url = 'http:' + \
                            seriesPart.xpath('h4/a/@href')[0].extract()

                        # 爬车系页面
                        request = scrapy.Request(
                            url=url, callback=self.parse_model_selling, dont_filter=True)
                        request.meta['brand_id'] = brand_id
                        request.meta['series_id'] = series_id
                        yield request
                    except:
                        pass

    def parse_model_selling(self, response):
        # brand_id = response.meta['brand_id']
        series_id = response.meta['series_id']
        # 循环发动机类型
        n = 1
        for enginePart in response.xpath('//div[@class="spec-wrap active"]/dl'):
            model_group = enginePart.xpath(
                'dt/div[1]/span/text()')[0].extract()
            # print "%s, %s, %s" % (brand_id, series_id, engine_type)
            # 循环车型
            for seriesPart in enginePart.xpath('dd'):
                model_name = seriesPart.xpath(
                    'div[1]/div/p[1]/a/text()')[0].extract()
                model_price = seriesPart.xpath(
                    'div[3]/p/span/text()')[0].extract()
                print "------------ %s, %s" % (model_name, model_price)

                modelItem = ModelItem()
                modelItem['group'] = model_group
                modelItem['series_id'] = series_id
                modelItem['id'] = series_id + "_" + str(n)
                modelItem['name'] = model_name
                modelItem['price'] = model_price
                n = n+1
                yield modelItem

                # print "----------------"

        for colorPart in response.xpath('//div[@class="athm-carcolor__inner"][1]/a'):

            color_name = colorPart.xpath('div[2]/text()')
            print "外观颜色 %s" % (color_name)

        # print response.xpath(
        #     '//div[@class="spec-wrap active"]/dl[1]/dd[1]/div/div/p[1]/a/text()').extract()
