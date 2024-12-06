import time
from baseSpider.baseSpider import BaseSpiderObject,RequestItem

class ahhyzb(BaseSpiderObject):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "aceg_zhaobiao"
    start_urls = 'https://cg.aceg.com.cn/inteligentsearch/rest/esinteligentsearch/getFullTextDataNew'
    
    
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = 'https://cg.aceg.com.cn'  # 用于拼接详情页网址
    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '安徽建工集团股份有限公司'
    source = 'cg.aceg.com.cn'

    data = {
        "token": "",
        "pn": 0,
        "rn": 9,
        "sdt": "",
        "edt": "",
        "wd": "%20",
        "inc_wd": "",
        "exc_wd": "",
        "fields": "title",
        "cnum": "001",
        "sort": "{\"webdate\":\"0\"}",
        "ssort": "title",
        "cl": 200,
        "terminal": "",
        "condition": [
            {
                "fieldName": "categorynum",
                "equal": "001",
                "notEqual": None,
                "equalList": None,
                "notEqualList": None,
                "isLike": True,
                "likeType": 2
            }
        ],
        "time": [
            {
                "fieldName": "webdate",
                "startTime": "1970-01-01 00:00:00",
                "endTime": "2999-12-31 23:59:59"
            }
        ],
        "highlights": "citycode",
        "statistics": None,
        "unionCondition": None,
        "accuracy": "",
        "noParticiple": "0",
        "searchRange": None,
        "isBusiness": "1"
}


    def start_requests(self):
               
            # 设置请求参数
            request_params = {
                'url': self.start_urls,
                'method': 'post',
                'request_body': 'json',
                'meta': {'page': 1,'use_playwright': True,},
                'callback': self.parse,
                'params': self.data
            }

            yield self.parse_task(RequestItem(**request_params))

    def parse(self, response):
        
        page = response.meta['page']

        node_list  = response.json()['result']['records']
       
        for node in node_list:

            baseItem = self.get_base_item()
            baseItem['title'] = node['title']
            baseItem['publish_time'] = node['infodate'][:10]
            baseItem['url'] = self.contents_base_urls + node['linkurl']

            request_params = {
                'url': baseItem['url'],
                'meta': {'item': baseItem},
                'callback': self.parse_content_detal,
                'errback': self.errback_httpbin,
            }


            # 判断是否继续爬取
            if self.calculate_task_item(baseItem):

                # 爬取详情页
                yield self.parse_task(RequestItem(**request_params))


        # 翻页,需要构建新的请求参数
        page += 1
        self.data['pn'] = page * 9
        request_params = {
                    'url': self.start_urls,
                    'method': 'post',
                    'request_body': 'json',
                    'meta': {'page': page},
                    'callback': self.parse,
                    'params': self.data
                }
        # 翻页
        yield self.request_next_page(baseItem, page, request_params)
        

