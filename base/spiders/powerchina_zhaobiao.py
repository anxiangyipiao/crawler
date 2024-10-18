import datetime
import json
import time
import scrapy
from urllib.parse import urlencode
# -------------------------------tag-------------------------------------------
# 这里需要在python安装目录\Lib\site-packages下创建 .pth文件，内容为sp_control.py的路径
from sp_action.sp_control import ZhaotoubiaoBaseSpider
from sp_action.items import SpiderItem

# 建设工程
class Shandong_JiNan_ggzy_jianshegongcheng_zhaobiao(ZhaotoubiaoBaseSpider):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "powerchina_zhaobiao"
    start_urls = 'https://ec.powerchina.cn/zgdjcms/category/bulletinList.html?searchDate=1999-10-10&dates=300&word=&categoryId=2&tabName=&purType=&startPublishDate=&endPublishDate=&page={page}'
    
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = 'https:'  # 用于拼接详情页网址
    page_urls = ""  # 用于获取下一页网址

    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '中国电建设备物资集中采购平台V3.0'
    source = 'ec.powerchina.cn'
    max_page = 10

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }

   
    def start_requests(self):

            urls = self.start_urls.format(page=1)
            yield scrapy.Request(urls,method='get',callback=self.parse,dont_filter=True,meta={'page':1},headers=self.headers)

    def parse(self, response):
        
        page = response.meta['page']
   
        node_list  = response.xpath('//ul[@id="bulletinList"]/li')
 
        for node in node_list:

            # 如果a标签没有href属性值，则跳过
            if node.xpath('./a/@href').extract_first() == None:
                continue
           
            item = SpiderItem()
            item['source'] = self.source
            item['site_name'] = self.site_name
            item['province'] = self.province
            item['city'] = self.city
            item['county'] = self.county
            item['title'] = node.xpath('./a/@title').extract_first().strip()
            item['publish_time'] = node.xpath('./a/div/div/text()').extract_first().strip()
            item['url'] = self.contents_base_urls + node.xpath('./a/@href').extract_first().strip()
          
            # -------------------------------tag-------------------------------------------
            add_task = self.add_download_task(item['url'],item['publish_time'])
            # 招标内容
            if add_task == False:

                yield scrapy.Request(item['url'], callback=self.parse_detail, meta={'item': item})
        # -------------------------------tag-------------------------------------------
        # 检查当页数据日期，判断是否翻页
        if node_list != None and len(node_list) > 0:
            check_publish_time = self.check_published_time(item['publish_time'])
            # print("check_publish_time:%s" % check_publish_time)
        # -------------------------------tag-------------------------------------------
        # if self.pagecount < int(self.max_page) and check_publish_time:
        if page < int(self.max_page) and check_publish_time:
            time.sleep(1)
            page += 1
            urls = self.start_urls.format(page=page)
            yield scrapy.Request(urls, method='get', callback=self.parse, dont_filter=True, meta={'page': page},headers=self.headers)
        else:
            # -------------------------------tag-------------------------------------------
            # 标记翻页结束
            self.page_over = True

    def parse_detail(self, response):
        # 获取详情页数据
        item = response.meta['item']
        item['contents'] = self.contents_base_urls + response.xpath('//iframe/@src').extract_first().strip()
        yield item
