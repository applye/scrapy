import scrapy
from scrapy.http import Request
from CrawlerMM.items import CrawlermmItem
import re
class MmonlySpider(scrapy.Spider):
    name = 'mmonly'
    allowed_domains = ['www.mmonly.cc']

    curl = 'https://www.mmonly.cc/tag/{}/index{}.html'
    # category = ['rili', 'dongman', 'fengjing', 'meinv', 'youxi', 'yingshi', 'dongtai', 'weimei', 'sheji', 'keai', 'qiche', 'huahui', 'dongwu', 'jieri', 'renwu', 'meishi', 'shuiguo', 'jianzhu', 'tiyu', 'junshi', 'feizhuliu', 'qita', 'wangzherongyao', 'huyan', 'lol']
    category = ['xfmn2']
    page_num = int(input('请输入要爬取的页码数(输入0表示爬取总页数)：'))
    page_index0 = ''
    i=0  # meinv
    j=1
    start_urls = [curl.format(category[i], page_index0)]
    print('开始：', start_urls)
    def parse(self, response):
        item = CrawlermmItem()
        hrefs = response.xpath('//*//div[@class="ABox"]/a/@href').getall()
        print(item)
        if self.page_num == 0:
            total_pages = int(response.xpath('//div[@class="pages"]//a/@href').extract()[-1])
            m = re.findall("\d+", total_pages[-1])
            self.page_num = m[0]
            print('总数：', total_pages)

        for i in hrefs[0:1]:
            yield Request(i, callback=self.downwith, meta={'item': item})
        if self.j < self.page_num:
            self.j+=1
            self.page_index = self.page_index0
            self.page_index += str(self.j)
            next_url = f'https://www.mmonly.cc/tag/{self.category[self.i]}/{self.page_index}.html'
            yield Request(url=next_url)
            print('开始爬取下一页内容。。。', self.page_index, next_url)
        else:
            self.i+=1
            if self.i < len(self.category):
                self.j = 1
                newUrl = self.curl.format(self.category[self.i], self.page_index0)
                yield Request(url=newUrl)
                print(f'开始爬取{self.category[self.i]}的内容。。。')

    def downwith(self,response):
        item = response.meta['item']
        dirName = response.xpath("//div[@class='topmbx']//a[last()]/text()").get()
        url = response.xpath('//*[@id="big-pic"]//img/@src').extract_first()
        name = response.xpath('//*[@id="big-pic"]//img/@alt').extract_first()
        total = response.xpath('//*[@id="picnum"]/span[last()]/text()').get()
        currPage = response.xpath('//*[@id="picnum"]/span[1]/text()').get()
        if url:
            item['dirName'] = f'{dirName}'
            item['name'] = name +''+ url.split('/')[-1]
            item['url'] = url
            print('downwith', item)
            yield item
        if(int(currPage) < int(total)):
            # 获取下一页
            nextUrl = response.xpath('//li[@id="nl"]/a/@href').get()
            nextUrl = response.urljoin(nextUrl)
            print('开始获取下一页',currPage, total, nextUrl)
            if('http' in nextUrl) :
                yield Request(nextUrl, callback=self.downwith, meta={'item': item})