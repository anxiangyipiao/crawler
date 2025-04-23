import time
from baseSpider.baseSpider import BaseSpiderObject,RequestItem


class Shandong_JiNan_ggzy_jianshegongcheng_zhaobiao(BaseSpiderObject):
    name = "ahdxpm_zhaobiao"
    start_urls = 'http://www.ahdxpm.com/articleListData'
    
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = 'http://www.ahdxpm.com/articleListDataDetail?id='  # 用于拼接详情页网址
    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '鼎信数智技术集团股份有限公司'
    source = 'www.ahdxpm.com'
    max_page = 10

    data = {
        "columnThreeId": "128",
        "page": "1",
        "rows": "10"
    }

    def start_requests(self):
        request_params = {
            'url': self.start_urls,
            'method': 'post',
            'request_body': 'formdata',
            'meta': {'page': 1},
            'callback': self.parse,
            'params': self.data
        }
        yield self.parse_task(RequestItem(**request_params))

    def parse(self, response):
        page = response.meta['page']
        node_list = response.json().get('rows', [])

        for node in node_list:
            baseItem = self.get_base_item()
            baseItem['title'] = node['title']
            baseItem['publish_time'] = node['createDate'][:10]
            baseItem['url'] = f"{self.contents_base_urls}{node['id']}"

            request_params = {
                'url': baseItem['url'],
                'meta': {'item': baseItem},
                'callback': self.parse_content_detal,
                'errback': self.errback_httpbin,
            }

            if self.calculate_task_item(baseItem):
                yield self.parse_task(RequestItem(**request_params))

        # 翻页逻辑
        if page < int(self.max_page) and node_list:
            page += 1
            self.data['page'] = str(page)
            request_params = {
                'url': self.start_urls,
                'method': 'post',
                'request_body': 'formdata',
                'meta': {'page': page},
                'callback': self.parse,
                'params': self.data
            }
            yield self.request_next_page(baseItem, page, request_params)