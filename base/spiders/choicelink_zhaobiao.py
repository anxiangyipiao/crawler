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
    name = "choicelink_zhaobiao"
    start_urls = 'https://middleware.choicelink.cn/notice/api/public/siteserverContent1/getIndex?'
    
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = 'https://middleware.choicelink.cn/notice/api/public/notice/queryNoticePublic?siteId={siteId}&channelId={channelId}&contentId={contentId}'  # 用于拼接详情页网址
    page_urls = ""  # 用于获取下一页网址

    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '云采链线上采购'
    source = 'middleware.choicelink.cn'
    max_page = 20

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }

    # 获取当前时间，以及前3天和后1天的时间
    now = datetime.datetime.now()
    three_days_ago = now - datetime.timedelta(days=2)
    one_day_later = now + datetime.timedelta(days=1)

    # 将时间转换为字符串格式
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    three_days_ago_str = three_days_ago.strftime('%Y-%m-%d')
    one_day_later_str = one_day_later.strftime('%Y-%m-%d')

    # 构建查询表单
    form = {
        "filter": "siteId == \"4795\" && channelId in \"5138\" && applyFromTime <= \"{now_str}\" && applyToTime >= \"{now_str}\" && ( addDate >= \"{three_days_ago_str} 00:00:00\" &&  addDate <= \"{one_day_later_str} 00:00:00\" )",
        "order": "addDate desc",
        "pageNum": "1",
        "pageSize": "30"
    }
    


   
    def start_requests(self):
            
            self.form['filter'] = self.form['filter'].format(now_str=self.now_str, three_days_ago_str=self.three_days_ago_str, one_day_later_str=self.one_day_later_str)

            urls = self.start_urls + urlencode(self.form)
            yield scrapy.Request(urls,method='get',callback=self.parse,dont_filter=True,meta={'page':1},headers=self.headers)

    def parse(self, response):
        
        page = response.meta['page']

        node_list  = response.json()['result']['items']
 
        for node in node_list:

            item = SpiderItem()
            item['source'] = self.source
            item['site_name'] = self.site_name
            item['province'] = self.province
            item['city'] = self.city
            item['county'] = self.county
            item['title'] = node['title']
            item['publish_time'] = node['addDate'][:10]
            item['url'] = self.contents_base_urls.format(siteId=node['siteId'],channelId=node['channelId'],contentId=node['id'])
          
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
            self.form['pageNum'] = str(page)
            urls = self.start_urls + urlencode(self.form)
            yield scrapy.Request(urls,method='get',callback=self.parse,dont_filter=True,meta={'page':page})
        else:
            # -------------------------------tag-------------------------------------------
            # 标记翻页结束
            self.page_over = True

    def parse_detail(self, response):
        # 获取详情页数据
        item = response.meta['item']
        item['contents'] = response.json()['value']['content']
        yield item
