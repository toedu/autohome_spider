#!/usr/bin/python
# coding=utf-8
import os
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

    # request_ids = [33]

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
        for brandPart in response.xpath('body/dl'):
            brand_id = brandPart.xpath('@id')[0].extract()

            if eval(brand_id) in self.request_ids:

                n = brandPart.xpath('dd/div[@class="h3-tit"]').extract()
                # print "-------- %d" % len(n)
                for i in range(len(n)):
                    # print i
                    s = 'dd/div[@class="h3-tit"][%d]/a/text()' % (i+1)
                    make_name = brandPart.xpath(s)[0].extract()
                    print "-------- %s" % make_name

                    seriesParts = brandPart.xpath(
                        'dd/ul[@class="rank-list-ul"][%d]/li' % (i+1))
                    for seriesPart in seriesParts:

                        try:
                            # 过滤无价格的车系
                            price = seriesPart.xpath(
                                'div/a/text()')[0].extract()
                            if len(price) == 2:
                                continue

                            # 爬车系颜色
                            url = 'http:' + \
                                seriesPart.xpath('h4/a/@href')[0].extract()
                            request = scrapy.Request(
                                url=url, callback=self.parse_color, dont_filter=True)
                            request.meta['brand_id'] = brand_id
                            request.meta['make_name'] = make_name
                            request.meta['series_id'] = seriesPart.xpath(
                                '@id')[0].extract()
                            request.meta['name'] = seriesPart.xpath(
                                'h4/a/text()')[0].extract()
                            request.meta['price'] = seriesPart.xpath(
                                'div/a/text()')[0].extract()
                            request.meta['url'] = seriesPart.xpath(
                                'h4/a/@href')[0].extract()
                            yield request
                            # yield series
                        except:
                            pass
            else:
                continue

    def parse_color(self, response):

        series_name = response.meta['name']
        print "---------------series_name: %s" % (series_name)
        # 循环发动机类型

        # 存储车系数据
        series = SeriesItem()
        series['brand_id'] = response.meta['brand_id']
        series['make_name'] = response.meta['make_name']
        series['id'] = response.meta['series_id']
        series['name'] = response.meta['name']
        series['price'] = response.meta['price']
        series['url'] = response.meta['url']

        out_colors = []
        for colorPart in response.xpath('//div[@class="series-picture"]/div[2]/div[2]/div[1]/div[1]/div[1]/a'):
            print colorPart.xpath('@href')[0].extract()
            color_name = colorPart.xpath('div[2]/text()')[0].extract()
            out_colors.append(color_name)
            print "外观颜色 %s" % (color_name)

        in_colors = []
        for colorPart in response.xpath('//div[@class="series-picture"]/div[2]/div[2]/div[2]/div[1]/div[1]/a'):
            print colorPart.xpath('@href')[0].extract()
            color_name = colorPart.xpath('div[2]/text()')[0].extract()
            in_colors.append(color_name)
            print "内饰 %s" % (color_name)

        series['colors'] = {'out': out_colors, 'in': in_colors}

        yield series
