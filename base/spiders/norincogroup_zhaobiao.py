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
    name = "norincogroup_zhaobiao"
    start_urls = 'https://bid.norincogroup-ebuy.com/retrieve.do'
    
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = ''  # 用于拼接详情页网址
    page_urls = ""  # 用于获取下一页网址

    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '阳光七采·兵纷招采电子招标投标交易平台'
    source = 'bid.norincogroup-ebuy.com'
    max_page = 2

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }

    params = {
    "fl": "",
    "hy": "",
    "dq": "",
    "es": "1",
    "keyFlag": "",
    "packtype": "",
    "packtypeCode": "",
    "packtypeValue": "",
    "packtypeCodeValue": "",
    "typflag": "1,2",
    "fbdays": "0",
    "esly": "",
    "validityPeriodFlag": "",
    "flag1": "",
    "orderby": "1",
    "keyConValue": "",
    "keyCon": "",
    "fbDateStart": "",
    "fbDateEnd": "",
    "radio": "on",
    # "ggyxq_time": "2024-10-21 08:00:00",
    "pageNumber": "2",
    "pageSize": "10",
    "sortColumns": "undefined"
}

   
    def start_requests(self):

        yield scrapy.FormRequest(self.start_urls,method='post',callback=self.parse,dont_filter=True,meta={'page':1},headers=self.headers,formdata=self.params)
      

    def parse(self, response):
        
        page = response.meta['page']

        node_list  = response.xpath('//div[@class="item"]')
 
        for node in node_list:

            item = SpiderItem()
            item['source'] = self.source
            item['site_name'] = self.site_name
            item['province'] = self.province
            item['city'] = self.city
            item['county'] = self.county
            item['title'] = node.xpath('.//a/@title').extract_first().strip()
            item['publish_time'] = node.xpath('.//ul[@class="list clearfix"]/li[3]/text()').extract_first().strip()[:10]
            item['url'] = node.xpath('.//a/@href').extract_first().strip()
          
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
            self.params['pageNumber'] = str(page)
            yield scrapy.FormRequest(self.start_urls,method='post',callback=self.parse,dont_filter=True,meta={'page':page},headers=self.headers,formdata=self.params)
        else:
            # -------------------------------tag-------------------------------------------
            # 标记翻页结束
            self.page_over = True

    def parse_detail(self, response):
        # 获取详情页数据
        item = response.meta['item']
        item['contents'] = response.text
        yield item
