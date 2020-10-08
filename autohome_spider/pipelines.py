# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


# 默认生成的pipeline，没有使用到
class AutohomeSpiderPipeline(object):
    def process_item(self, item, spider):
        return item



class ImagespiderPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
    	imgName = item['tag'] + '_' + item['id'] + ".jpg"
    	yield Request(item['imgUrl'], meta={'name':imgName})

        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        # for image_url in item['imgurl']:
            # yield Request(image_url)

    def file_path(self, request, response=None, info=None):
    	imgName = request.meta['name']
    	return 'brand/' + imgName