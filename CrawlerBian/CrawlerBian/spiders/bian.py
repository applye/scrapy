import scrapy
from CrawlerBian.items import CrawlerbianItem
from scrapy import Request
class BianSpider(scrapy.Spider):
    name = 'bian'
    allowed_domains = ['netbian.com']
    # allowed_domains = ['pic.netbian.com']
    # start_urls = ['https://pic.netbian.com/4kmeinv/']
    curl = 'http://www.netbian.com/{}/index{}.htm'
    # category = ['rili', 'dongman', 'fengjing', 'meinv', 'youxi', 'yingshi', 'dongtai', 'weimei', 'sheji', 'keai', 'qiche', 'huahui', 'dongwu', 'jieri', 'renwu', 'meishi', 'shuiguo', 'jianzhu', 'tiyu', 'junshi', 'feizhuliu', 'qita', 'wangzherongyao', 'huyan', 'lol']
    category = ['meinv', 'feizhuliu']
    page_num = int(input('请输入要爬取的页码数(输入0表示爬取总页数)：'))
    page_index0 = ''
    i=0  # meinv
    j=1
    start_urls = [curl.format(category[i], page_index0)]
    print('开始：', start_urls)
    def parse(self, response):
        item = CrawlerbianItem()
        hrefs = response.xpath('//*[@id="main"]/div/ul/li/a/@href').getall()
        # item['dirName'] = response.xpath("//div[@class='classify clearfix']/a[@class='curr']/text()").get()
        item['dirName'] = response.xpath("//div[@id='main']//h1/text()").get()
       # 获取每个分类的总页数
        if self.page_num == 0:
            total_pages = response.xpath('//div[@class="pages"]//a/@href').extract()[-1]
            total_pages =  "https://www.mmonly.cc/tag/yyls/4.html"
            self.page_num = total_pages
            print('总数：', total_pages)

        for href in hrefs:
            url = response.urljoin(href)
            yield Request(url, callback=self.donwith, meta={'item': item})
        # nextPage = response.xpath("//div[@class='page']/a[last()-1]/@href").get()
        # next_page = response.urljoin(next_page)  # 拼接链接

        # lists = response.xpath("//ul[@class='clearfix']/li")
        # for i in lists:
        #     url = i.xpath('/a/img/@src').get()
        #     if url:
        #         src = url.repace('small', '')
        #         src = src[0:-14] + '.jpg'
        #         name = src.split('/')[-1]
        #         item = CrawlerbianItem()
        #         print(name, src)
        #         item['url'] = src
        #         item['name'] = name
        #         yield item
      
        # item['url'] = response.xpath("//ul[@class='clearfix']/li/a/img/@src").getall()
        # item['name'] = response.xpath("//ul[@class='clearfix']/li/a/img/@alt").getall()
        # item['dirName'] = response.xpath("//div[@class='classify clearfix']/a[@class='curr']/text()").get()
        # yield item

        # 下一页
        # nextPage = response.xpath("//div[@class='page']/a[last()]/@href").get()
        # print('nextPage', nextPage)
        # if 'index_2' in nextPage:
        #     print('page', nextPage)
        #     yield response.follow(nextPage, callback=self.parse)
        # pass
        # 下一页方式二
        if self.j < self.page_num:
            self.j+=1
            self.page_index = self.page_index0
            self.page_index += '_'+str(self.j)
            next_url = f'http://www.netbian.com/{self.category[self.i]}/index{self.page_index}.htm'
            yield Request(url=next_url)
            print('开始爬取下一页内容。。。', self.page_index, next_url)
        else:
            self.i+=1
            if self.i < len(self.category):
                self.j = 1
                newUrl = self.curl.format(self.category[self.i], self.page_index0)
                yield Request(url=newUrl)
                print(f'开始爬取{self.category[self.i]}的内容。。。')


    def donwith(self,response):
        item = response.meta['item']
        # url = response.xpath('//div[@class="photo-pic"]/a/img/@src').extract_first()
        
        # name = response.xpath('//div[@class="photo-pic"]/a/img/@title').extract_first()
        # 第二种
        url = response.xpath('//*[@id="main"]//div[@class="pic"]//a/img/@src').extract_first()
        name = response.xpath('//*[@id="main"]//div[@class="pic"]//a/img/@title').extract_first()
        if name:
            item['name'] = name
            item['url'] = response.urljoin(url)
            yield item

        
