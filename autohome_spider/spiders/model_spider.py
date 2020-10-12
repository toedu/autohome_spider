#!/usr/bin/python
# coding=utf-8
import os
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

    request_ids = [33, 35, 34, 327, 36, 14, 15, 38, 75, 40, 120, 13, 27, 39, 95, 154, 173, 208, 231, 203, 79, 392, 387, 301, 271, 351, 76, 77, 163, 294, 299, 366, 196, 1, 165, 32, 113, 259, 169, 405, 142, 81, 341, 326, 3, 8, 96, 42, 416, 434, 141, 197, 82, 152, 329, 376, 313, 112, 383, 369, 181, 91, 86, 150, 267, 97, 164, 386, 429, 25, 46, 44, 84, 358, 319, 119, 83, 270, 145, 373, 419,
                   151, 175, 356, 47, 9, 214, 101, 156, 213, 109, 199, 52, 279, 49, 51, 53, 345, 54, 48, 10, 78, 88, 80, 335, 124, 215, 58, 20, 57, 56, 129, 381, 309, 60, 331, 308, 26, 62, 122, 312, 210, 63, 19, 296, 67, 68, 155, 65, 330, 325, 69, 306, 426, 162, 269, 433, 133, 400, 339, 161, 114, 70, 283, 284, 167, 291, 393, 192, 12, 71, 72, 350, 396, 275, 324, 73, 110, 144, 111, 263, 286, 398, 74, 22]
    total = 0
    saved = 0

    def __init__(self):
        path = 'data/%s.json' % (self.name)
        if os.path.exists(path):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            os.remove(path)
        else:
            print('no such file:%s' % path)  # 则返回文件不存在
        print 'start'

    def parse(self, response):
        # 循环品牌
        for brandPart in response.xpath('body/dl'):
            brand_id = brandPart.xpath('@id')[0].extract()

            if eval(brand_id) in self.request_ids:
                # 循环厂商
                n = brandPart.xpath('dd/div[@class="h3-tit"]').extract()
                for i in range(len(n)):
                    # 循环车系
                    seriesParts = brandPart.xpath(
                        'dd/ul[@class="rank-list-ul"][%d]/li' % (i+1))
                    for seriesPart in seriesParts:
                        try:
                            # 过滤无价格的车系
                            price = seriesPart.xpath(
                                'div/a/text()')[0].extract()
                            if len(price) == 2:
                                print('***********')
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

            else:
                continue

    def parse_model_selling(self, response):
        # brand_id = response.meta['brand_id']
        series_id = response.meta['series_id']
        print "series_id: %s" % (series_id)
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
                # print "------------ %s, %s" % (model_name, model_price)

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

            color_name = colorPart.xpath('div[2]/text()')[0].extract()
            print "外观颜色 %s" % (color_name)

        # print response.xpath(
        #     '//div[@class="spec-wrap active"]/dl[1]/dd[1]/div/div/p[1]/a/text()').extract()
