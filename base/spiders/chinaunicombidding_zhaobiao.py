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
    name = "chinaunicombidding_zhaobiao"
    start_urls = 'http://www.chinaunicombidding.cn/api/v1/bizAnno/getAnnoList?Wlfknewu=7gYmUalqEET3B_K14e5JFpbrtGmG8bs9G4.JDDCj9pAtuASXpeDmEtnTbvXlK0SNKIhUcR1iq4rkOOfRAWsSMBD.9hSRr61r'
    
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = 'http://www.chinaunicombidding.cn/bidInformation/detail?id={id}'  # 用于拼接详情页网址
    page_urls = ""  # 用于获取下一页网址

    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '中国联通采购与招标网'
    source = 'www.chinaunicombidding.cn'
    max_page = 2

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'content-type':'application/json;charset=UTF-8',
        "host":"www.chinaunicombidding.cn",
        "origin":"http://www.chinaunicombidding.cn",
        "proxy-connection":"keep-alive",
        "referer":"http://www.chinaunicombidding.cn/bidInformation",
        'accept':'application/json',
        'roleid':'',
        'cookie':
'jqmEwVYRfTEJS=5l_n7oQGK90QJefmmTC0kmGmpkW9g9YeGL9jZwLqG5En8SvrPkAMELKVp5AwLnmWIs0LlVVHPHtCZTpq5GC1tEG; MY_COOKIE=N1Tz2w45Uz+8aeIZxRf1QJv0jE+xS4cuI6mEmTnLY8h1bm6oOHIlEwUVmCYCSDeYQbFzmKYatHdowQ==; BIGipServerPOOL_CAIGOU3=214761482.16671.0000; jqmEwVYRfTEJT=iOLfO0N_joWTHWjtcSKg_tutE.C8E60fw_FQZvGh6414UUwTbvWC4eXgBzQSWAthaRwTitJkwlcJ_._tKhQ5bi.CKry6yV6In4j6W7qHj1lWEIpVx4e8gnD7fiP.PWldrgEztee8ETYkB4IFi9CmenLShhsxX82UDTaTO_O_A_svX7sVotGDpxmT1xxFEZpcWEzqlcwOsiJPjGpE7q.1F9k7IF229agQpdeumRBaGQvD7eVD_W1.21ggx8gGl6mn9Dxnyx7KOvNsTq4Gv.DhkTNWOcR2b2x6BXS0AK.YFQZR86miLUi4YPaajajH5_l7hGsLDHkv9xElAcey3t4ew5u7ysojF0UJSRhheUyT7LfgVpGAQi5nxa7MC8secqHnEq96YUbk.pFeHOkX6Ubj4er8JjKkGp2LWMRyCm_Y._L'
    }

    form = {
    "current": 1,
    "pageSize": 10,
    "modeNo": "BizAnnoVoMtable",
    "pageNo": 1,
    "annoType": "001001"
}

   
    def start_requests(self):

            yield scrapy.Request(self.start_urls,method='post',body=json.dumps(self.form),callback=self.parse,dont_filter=True,meta={'page':1},headers=self.headers)

    def parse(self, response):
        
        page = response.meta['page']

        node_list  = response.json()['data']['records']
 
        for node in node_list:

            item = SpiderItem()
            item['source'] = self.source
            item['site_name'] = self.site_name
            item['province'] = self.province
            item['city'] = self.city
            item['county'] = self.county
            item['title'] = node['title']
            item['publish_time'] = node['createDate'][:10]
            item['url'] = self.contents_base_urls.format(id=node['id'])
          
            # -------------------------------tag-------------------------------------------
            add_task = self.add_download_task(item['url'],item['publish_time'])
            # 招标内容
            if add_task == False:

                next_url = 'http://www.chinaunicombidding.cn/api/v1/bizAnno/getAnnoDetailed/{id}'.format(id=node['id'])
                yield scrapy.Request(next_url, callback=self.parse_detail, meta={'item': item})
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
            self.form['current'] = page
            self.form['pageNo'] = page
            yield scrapy.Request(self.start_urls,method='post',body=json.dumps(self.form),callback=self.parse,dont_filter=True,meta={'page':page},headers=self.headers)
        else:
            # -------------------------------tag-------------------------------------------
            # 标记翻页结束
            self.page_over = True

    def parse_detail(self, response):
        # 获取详情页数据
        item = response.meta['item']
        item['contents'] = response.json()['data']['annoText']
        yield item
