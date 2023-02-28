# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests
from scrapy.pipelines.images import ImagesPipeline
import scrapy

class CrawlermmPipeline:
    def process_item(self, item, spider):
        print('222', item)
        return item

class SaveImagePipline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['url'], meta={"name": item['name'], 'dirName': item['dirName']})
    def file_path(self, request, response=None, info=None, *, item=None):
        imgname = request.meta['name'].strip()
        dirname = request.meta['dirName']
        filename = f"{dirname}/{imgname}"
        return filename
    def item_completed(self, requests, item, info):
        return item