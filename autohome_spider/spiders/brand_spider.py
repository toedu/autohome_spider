#!/usr/bin/python
# coding=utf-8

import os
import scrapy
from autohome_spider.items import BrandItem
# from scrapy import log


# 品牌数据爬虫
class BrandSpider(scrapy.Spider):
    name = 'brand'
    allowed_domains = 'autohome.com.cn'
    start_urls = ['http://www.autohome.com.cn/grade/carhtml/%s.html' %
                  chr(ord('A') + i) for i in range(26)]

    custom_settings = {
        'FEED_URI': 'data/%(name)s.json',

        'ITEM_PIPELINES': {
            'autohome_spider.pipelines.ImagespiderPipeline': 1,
            # 'autohome_spider.pipelines.BrandJsonPipeline': 2,
        }
    }

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
        print "URL: " + response.request.url
        url = response.request.url
        tag = url[-6:-5]
        # print "tag: " + tag

        for brandPart in response.xpath('body/dl'):
            brand_id = brandPart.xpath('@id')[0].extract()
            brand_name = brandPart.xpath('dt/div/a/text()')[0].extract()
            self.total = self.total + 1
            if eval(brand_id) in self.request_ids:
                print '.....保存品牌数据： %s' % (brand_name)
                self.saved = self.saved + 1

                brand = BrandItem()
                brand['tag'] = tag
                brand['id'] = brandPart.xpath('@id')[0].extract()
                # brand['url'] = brandPart.xpath('dt/a/@href')[0].extract()
                brand['name'] = brandPart.xpath('dt/div/a/text()')[0].extract()
                brand['imgUrl'] = "https:" + \
                    brandPart.xpath('dt/a/img/@src')[0].extract()
                yield brand

            else:
                continue

    def closed(self, reason):
        print '---------- total: %d, saved: %d' % (self.total, self.saved)
