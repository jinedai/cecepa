# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import json
import codecs

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('cecepa.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

class DownloadImagesPipeline(ImagesPipeline):
    def get_media_requests(self,item,info): #下载图片
        for image_url in item['imageurl']:
            yield Request(image_url,meta={'item':item}) #添加meta是为了下面重命名文件名使用

    def file_path(self,request,response=None,info=None):
        item=request.meta['item'] #通过上面的meta传递过来item

        #图片文件名，item['carname'][index]得到汽车名称，request.url.split('/')[-1].split('.')[-1]得到图片后缀jpg,png
        image_guid = request.url.split('/')[-1]
        #图片下载目录 此处item['country']即需要前面item['country']=''.join()......,否则目录名会变成\u97e9\u56fd\u6c7d\u8f66\u6807\u5fd7\xxx.jpg
        filename = u'full/{0}/{1}'.format(item['albumname'], image_guid) 
        return filename

