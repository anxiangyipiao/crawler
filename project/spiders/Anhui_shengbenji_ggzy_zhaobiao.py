from baseSpider.baseSpider import BaseSpiderObject,RequestItem
import re


class Anhui_shengbenji_jianshegongcheng_zhaobiaoSpider(BaseSpiderObject):
    name = "Anhui_shengbenji_ggzy_zhaobiao"
    start_urls = 'https://ggzy.ah.gov.cn/jsgc/list'  # 必填，爬虫开始网址
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = 'https://ggzy.ah.gov.cn'  # 用于拼接详情页网址
    page_urls = ""  # 用于获取下一页网址
    form_data = {
        'currentPage': '1',
        'tenderProjectType': '1',
        'bulletinNature': '1',
        'jyptId': '',
        'region': '',
    }

    province = "安徽省"  # 必填，爬虫省份
    city = ""
    county = ""  # 选填，爬虫区/县
    site_name = '安徽省公共资源交易监管网'
    source = 'ggzy.ah.gov.cn'
    pagecount = 1  # 用于爬取下一页
    max_page = 50
    detail_data = {
        'type': 'tender',
        'bulletinNature': '1',
        'guid': '',
        'statusGuid': '',
    }
    detail_url = 'https://ggzy.ah.gov.cn/jsgc/newDetailSub'
    li = ['1', '2', '3', '4']

    def start_requests(self):
        for i in self.li:
            self.form_data['tenderProjectType'] = i 
            request_params = {
                'url': self.start_urls,
                'method': 'post',
                'request_body': 'formdata',
                'params': self.form_data,
                'meta': {'equal': i, 'page_now': 1},
                'callback': self.parse,
            }
            yield self.parse_task(RequestItem(**request_params))

    def parse(self, response):
        equal = response.meta.get('equal')
        page_now = response.meta.get('page_now', 1)

        node_list = response.xpath('//div[@class="list clear"]/ul/li')[1:]

        for node in node_list:
            baseItem = self.get_base_item()
            baseItem['title'] = node.xpath("./a/span/@title").extract_first()
            baseItem['publish_time'] = node.xpath("./span/text()").extract_first()
            baseItem['url'] = self.contents_base_urls + node.xpath("./a/@href").extract_first()
            guid = re.findall('guid=(.*?)&', baseItem['url'], re.DOTALL)[0]
            self.detail_data['guid'] = guid

            request_params = {
                    'url': self.detail_url,
                    'method': 'post',
                    'request_body': 'formdata',
                    'params': self.detail_data,  
                    'meta': {'item': baseItem},
                    'callback': self.parse_content_detal,
                    'errback': self.errback_httpbin,
                }
            if self.calculate_task_item(baseItem):

                yield self.parse_task(RequestItem(**request_params))

        page_now += 1
        self.form_data['tenderProjectType'] = equal
        self.form_data['currentPage'] = str(page_now)
        request_params = {
                'url': self.start_urls,
                'method': 'post',
                'request_body': 'formdata',
                'params': self.form_data, 
                'meta': {'equal': equal, 'page_now': page_now},
                'callback': self.parse,
        }
        yield self.request_next_page(baseItem, page_now, request_params)

 