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
    name = "chinatelecom_zhaobiao"
    start_urls = 'https://caigou.chinatelecom.com.cn/portal/base/announcementJoin/queryListNew'
    
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = 'https://caigou.chinatelecom.com.cn/DeclareDetails?id={id}&type=1&docTypeCode={TypeCode}'  # 用于拼接详情页网址
    page_urls = ""  # 用于获取下一页网址

    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '中国电信阳光采购平台'
    source = 'caigou.chinatelecom.com.cn'
    max_page = 10

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'content-type':'application/json;charset=UTF-8',
    }

    form = {
    "pageNum": 1,
    "pageSize": 10,
    "type": "e2no",
    "queryStartTime": "",
    "provinceCode": ""
}
    
    def start_requests(self):

            yield scrapy.Request(self.start_urls,method='post',body=json.dumps(self.form),callback=self.parse,dont_filter=True,meta={'page':1},headers=self.headers)

    def parse(self, response):
        
        page = response.meta['page']
    
        node_list  = response.json()['data']['list']
 
        for node in node_list:

            item = SpiderItem()
            item['source'] = self.source
            item['site_name'] = self.site_name
            item['province'] = self.province
            item['city'] = self.city
            item['county'] = self.county
            item['title'] = node['docTitle']
            item['publish_time'] = node['createDate'][:10]

            
            item['url'] = self.contents_base_urls.format(id=node['docId'],TypeCode=node['docTypeCode'])

          
            # -------------------------------tag-------------------------------------------
            add_task = self.add_download_task(item['url'],item['publish_time'])
            # 招标内容
            if add_task == False:
            
                content_url = 'https://caigou.chinatelecom.com.cn/portal/base/'+ node['docTypeCode'].lower() +"/"+ node['docId']
                
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
            self.form['pageNum'] = page
            yield scrapy.Request(self.start_urls,method='post',body=json.dumps(self.form),callback=self.parse,dont_filter=True,meta={'page':page},headers=self.headers)
            
        else:
            # -------------------------------tag-------------------------------------------
            # 标记翻页结束
            self.page_over = True

    def parse_detail(self, response):
        # 获取详情页数据
        item = response.meta['item']

        if response.json()['data']['context'] != '':
            item['contents'] = response.json()['data']['context']
        else:
            item['contents'] = response.json()['data']['listPackage'][0]['packageContent']
            
        yield item
