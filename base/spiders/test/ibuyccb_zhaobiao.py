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
    name = "ibuyccb_zhaobiao"
    start_urls = 'https://ibuy.ccb.com/cms/channel/ccbbidzbgg/index.htm'
    
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = 'https://ibuy.ccb.com'  # 用于拼接详情页网址
    page_urls = ""  # 用于获取下一页网址

    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '中国建设银行'
    source = 'ibuy.ccb.com'
    max_page = 2

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'content-type':'application/x-www-form-urlencoded',
        'referer':'https://ibuy.ccb.com/cms/channel/ccbbidzbgg/index.htm',

    }

    params = {
    "pageNo": "1",
    "_ser_p": '',
    "keyword": "",
    "org": "",
    "area": "",
    "beginDate": "",
    "endDate": ""
}
    

    publickey = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCzrjWyZGR7kNdlnjDYptEB9mEc10NU53muUM/0vbzD8ivekX5zuJ6P7VrjzT7VIu1r9U9B2+xXzSF+2tinEzBpE8z/DAeL235ZmNUQJFIVGvrGUYs4q7nj21n4qNlwfbjpEH2kPkBG3jgAeEHMXj4tkaI5Nb/6Kr+yCZpaSn2U+wIDAQAB'
   

    def ras_encrypt(self,data):
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_v1_5
        import base64
        rsa_key = RSA.importKey(base64.b64decode(self.publickey))
        cipher = PKCS1_v1_5.new(rsa_key)
        cipher_text = base64.b64encode(cipher.encrypt(data.encode()))
        return cipher_text.decode()


    def start_requests(self):
        
        self.params['_ser_p'] = self.ras_encrypt(self.params['pageNo'])


        yield scrapy.FormRequest(self.start_urls,method='post',formdata=self.params,callback=self.parse,dont_filter=True,meta={'page':1},headers=self.headers)

           

    def parse(self, response):
        
        page = response.meta['page']
        

        node_list  = response.xpath('//div[@class="infolist-main single-main bidlist"]/ul/li')
 
        for node in node_list:

            item = SpiderItem()
            item['source'] = self.source
            item['site_name'] = self.site_name
            item['province'] = self.province
            item['city'] = self.city
            item['county'] = self.county
            item['title'] = node.xpath('./a/span/text()').extract_first().strip()
            item['publish_time'] = ''.join(node.xpath('./a/em//text()').getall()).strip()
            item['url'] = self.contents_base_urls + node.xpath('./a/@hrefurl').extract_first().strip()
          
            # -------------------------------tag-------------------------------------------
            add_task = self.add_download_task(item['url'],item['publish_time'])
            # 招标内容
            if add_task == False:

                pageNo = item['url'].split('/')[-1].split('.')[0]
                
                data = {
                    'pageNo': pageNo,
                    "_ser_p": self.ras_encrypt(pageNo),
                }

                content_url = item['url'] + '?%s' % urlencode(data)

                yield scrapy.Request(content_url, callback=self.parse_detail, meta={'item': item},headers=self.headers)
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
            self.params['pageNo'] = str(page)
            yield scrapy.FormRequest(self.start_urls,method='post',formdata=self.params,callback=self.parse,dont_filter=True,meta={'page':page},headers=self.headers)
        else:
            # -------------------------------tag-------------------------------------------
            # 标记翻页结束
            self.page_over = True

    def parse_detail(self, response):
        # 获取详情页数据
        item = response.meta['item']
        item['contents'] = response.text
        yield item
