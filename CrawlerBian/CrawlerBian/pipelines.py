# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
import requests
import os
from scrapy.pipelines.images import ImagesPipeline

# class CrawlerbianPipeline:
    # def process_item(self, item, spider):
        # for i in range(len(item['url'])):
            # imgUrl = "http://pic.netbian.com" + item['url'][i]
            # print(imgUrl, item['url'][i])
            # dirName = item['dirName']
            # yield scrapy.Request(imgUrl, meta={'name': item['name'][i], 'dirName': item['dirName']})
            # b_resp = requests.get(imgUrl, headers={
            #     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            #     })
     
            # if not os.path.exists(dirName):
            #     os.mkdir(dirName)
            
            # with open(dirName + "/"+ item['name'][i] + '.jpg', 'wb') as f:
            #     f.write(b_resp.content)

        #  方法二
        # print(item)
        # dirName = item['dirName']
        # name = item['name']
        # url = item['url']
        # if not os.path.exists(dirName):
        #     os.mkdir(dirName)

        # file = f'{dirName}/{name}.jpg'
        
        # if os.path.exists(file):
        #     print('文件已存在：', file)
        # else :
        #     print('开始下载文件：', url)
        #     b_resp = requests.get(url, headers={
        #         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        #         })
        #     with open(file, 'wb') as f:
        #         f.write(b_resp.content)


        #     # 给图片定义存放位置和图片名
        # pass
        # 方法三
        # return item
  
class SaveImagePipline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['url'], meta={"name": item['name'], 'dirName': item['dirName']})
    def file_path(self, request, response=None, info=None, *, item=None):
        imgname = request.meta['name'].strip() + '.jpg'
        dirname = request.meta['dirName']
        filename = f"{dirname}/{imgname}"
        return filename
    def item_completed(self, requests, item, info):
        return item