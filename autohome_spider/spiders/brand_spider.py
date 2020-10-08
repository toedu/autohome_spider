#!/usr/bin/python
# coding=utf-8

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

    def parse(self, response):
        print "URL: " + response.request.url
        url = response.request.url
        tag = url[-6:-5]
        print "tag: " + tag
        for brandPart in response.xpath('body/dl'):
            brand = BrandItem()
            brand['tag'] = tag
            brand['id'] = brandPart.xpath('@id')[0].extract()
            # brand['url'] = brandPart.xpath('dt/a/@href')[0].extract()

            # scrapy.log.msg("dddddddddddfff")
            # brand['name'] = brandPart.xpath('dt/div/a/text()')[0]
            brand['name'] = brandPart.xpath('dt/div/a/text()')[0].extract()
            brand['imgUrl'] = "https:" + \
                brandPart.xpath('dt/a/img/@src')[0].extract()
            yield brand
