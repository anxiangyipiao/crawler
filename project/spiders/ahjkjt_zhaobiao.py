from baseSpider.baseSpider import BaseSpiderObject, RequestItem

class Shandong_JiNan_ggzy_jianshegongcheng_zhaobiao(BaseSpiderObject):
    name = "ahjkjt_zhaobiao"
    start_urls = 'https://www.ahjkjt.com/info/index/cid/164/page/{page}'
    
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = 'https://www.ahjkjt.com'  # 用于拼接详情页网址
    page_urls = ""  # 用于获取下一页网址

    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '安徽省交通控股集团有限公司'
    source = 'www.ahjkjt.com'
    max_page = 10

  
    def start_requests(self):
        request_params = {
            'url': self.start_urls.format(page=1),
            'meta': {'page': 1},
            'callback': self.parse,
        }
        yield self.parse_task(RequestItem(**request_params))

    def parse(self, response):
        page = response.meta['page']

        node_list = response.xpath('//ul[@class="list"]/li')

        for node in node_list:
            baseItem = self.get_base_item()
            baseItem['title'] = node.xpath('./a/@title').extract_first()
            baseItem['publish_time'] = node.xpath('./span/text()').extract_first()
            baseItem['url'] = self.contents_base_urls + node.xpath('./a/@href').extract_first()

            request_params = {
                'url': baseItem['url'],
                'meta': {'item': baseItem},
                'callback': self.parse_content_detal,
                'errback': self.errback_httpbin,
            }

            if self.calculate_task_item(baseItem):
                yield self.parse_task(RequestItem(**request_params))

        
        # 翻页逻辑
        page += 1
        param = self.start_urls.format(page=page)
        request_params = {
                'url': param,
                'meta': {'page': page},
                'callback': self.parse,
        }
        yield self.request_next_page(baseItem, page, request_params)