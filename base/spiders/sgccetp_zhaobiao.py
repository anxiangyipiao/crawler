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
    name = "sgccetp_zhaobiao"
    start_urls = 'https://sgccetp.com.cn/ecpwcmcore/index/noteList'
    
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = 'https://sgccetp.com.cn/portal/#/doc/doci-bid/{id}_2018032700291334_{firstPageDocId}/old'  # 用于拼接详情页网址
    page_urls = ""  # 用于获取下一页网址

    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '中国南方电网有限责任公司'
    source = 'sgccetp.com.cn'
    max_page = 10

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }

    form = {
    "index": 1,
    "size": 20,
    "firstPageMenuId": "2018032700291334",
    "purOrgStatus": "",
    "purOrgCode": "",
    "purType": "",
    "orgId": "",
    "key": "",
    "homePageType": "1",
    "orgName": ""
}
   
    def start_requests(self):

        yield scrapy.Request(self.start_urls,method='post',callback=self.parse,dont_filter=True,meta={'page':1},headers=self.headers,body=json.dumps(self.form))

    def parse(self, response):
        
        page = response.meta['page']
        node_list  = response.json()['resultValue']['noteList']
 
        for node in node_list:

            item = SpiderItem()
            item['source'] = self.source
            item['site_name'] = self.site_name
            item['province'] = self.province
            item['city'] = self.city
            item['county'] = self.county
            item['title'] = node['title']
            item['publish_time'] = node['noticePublishTime'][:10]
            item['url'] = self.contents_base_urls.format(id=node['id'],firstPageDocId=node['firstPageDocId'])
 
            # -------------------------------tag-------------------------------------------
            add_task = self.add_download_task(item['url'],item['publish_time'])
            # 招标内容
            if add_task == False:

                yield scrapy.Request(item['url'],method='get',callback=self.parse_detail,dont_filter=True,meta={'item':item},headers=self.headers)
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
            self.form['index'] = page
            yield scrapy.Request(self.start_urls,method='post',callback=self.parse,dont_filter=True,meta={'page':page},headers=self.headers,body=json.dumps(self.form))
        else:
            # -------------------------------tag-------------------------------------------
            # 标记翻页结束
            self.page_over = True

    def parse_detail(self, response):
        # 获取详情页数据
        item = response.meta['item']
        item['contents'] = response.text
        yield item
