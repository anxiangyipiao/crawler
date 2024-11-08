import scrapy
import json
import time
from baseSpider.baseSpider import BaseSpiderObject,RequestItem

class Anhui_shengbenji_zbtbxxw_zhaobiaoSpider(BaseSpiderObject):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "Anhui_shengbenji_zbtbxxw_zhaobiao"
    start_urls = 'https://www.ahtba.org.cn/site/trade/affiche/pageList'  # 必填，爬虫开始网址
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = "https://www.ahtba.org.cn"  # 用于拼接详情页网址
    detail_url = "https://www.ahtba.org.cn/htmlUrl/trade_/{}/{}.html"

    form_data = {
        "afficheSourceType": '',
        "afficheTitle": '',
        "pageNum": 1,
        "pageSize": 10,
        "publishTimeType": 'year',
        "regionCode": '',
        "tradeType": ''
    }

    province = "安徽省"  # 必填，爬虫省份
    city = ""
    county = ""  # 选填，爬虫区/县
    site_name = '安徽省招标投标信息网'
    source = 'www.ahtba.org.cn'
    max_page = 100

    def start_requests(self):
        
        self.form_data['t'] = str(int(time.time() * 1000))
        
        # 设置请求参数
        request_params = {
                'url': self.start_urls,
                'method': 'post',
                'request_body': 'json',
                'meta': {'page': 1},
                'callback': self.parse,
                'params': self.form_data
            }
        
        yield self.parse_task(RequestItem(**request_params))

    def parse(self, response):
        page_now = response.meta.get('page_now', 1)
        node_list = response.xpath("//div[@class='rightBoxList']//li")

        for node in node_list:
            baseItem = self.get_base_item()
            baseItem['title'] = node.xpath(".//a/text()").extract_first().strip()
            baseItem['publish_time'] = node.xpath(".//div[@class='fr nums']/text()").extract_first().strip()
            baseItem['url'] = self.contents_base_urls + node.xpath(".//a/@href").extract_first().strip()
            
            detail_id = baseItem['url'].split('/')[-1]

            request_params = {
                'url': self.detail_url.format(baseItem['publish_time'], detail_id),
                'meta': {'item': baseItem},
                'callback': self.parse_content_detal,
                'errback': self.errback_httpbin,
            }
            if self.calculate_task_item(baseItem):

                yield self.parse_task(RequestItem(**request_params))

        page_now += 1
        self.form_data['pageNum'] = page_now
        request_params = {
                'url': self.start_urls,
                'method': 'post',
                'request_body': 'json',
                'meta': {'page': page_now},
                'callback': self.parse,
                'params': self.form_data
            }
        # 翻页
        yield self.request_next_page(baseItem, page_now, request_params)