import time
from baseSpider.baseSpider import BaseSpiderObject,RequestItem

class Henan_Pindingshan_ggzy_zhaobiaoSpider(BaseSpiderObject):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "Pindingshan"
    start_urls = [
         "http://ggzy.pds.gov.cn/zzbgg/index_{page}.jhtml",
        'http://ggzy.pds.gov.cn/gzbgg/index_{page}.jhtml',
    ]
    
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = 'http://ggzy.pds.gov.cn'  # 用于拼接详情页网址
    province = "河南省"  # 必填，爬虫省份
    city = "平顶山市"  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '平顶山市公共资源交易中心'
    source = 'ggzy.pds.gov.cn'

    def start_requests(self):

        for url in self.start_urls:
            
            time.sleep(1)
            full_url = url.format(page=1)
     
            # 设置请求参数
            request_params = {
                'request_body': None,
                'url': full_url,
                'method': 'GET',
                'meta': {'page': 1, 'param': url,'use_playwright': False},
                'callback': self.parse,
                'cookies': None,
                'headers': None,
                'params': None
            }

            yield self.parse_task(RequestItem(**request_params))

    def parse(self, response):
        
        param = response.meta['param']
        page = response.meta['page']

        node_list  = response.xpath('//div[@class="channel_list"]/ul/li')
       
        for node in node_list:

            baseItem = self.get_base_item()
            baseItem['title'] = node.xpath('./a/@title').extract_first().strip()
            baseItem['publish_time'] = node.xpath('./span/text()').extract_first()
            baseItem['url'] = self.contents_base_urls + node.xpath('./a/@href').extract_first()

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
        request_params = {
                    'url': param.format(page=page),
                    'method': 'GET',
                    'meta': {'page': page, 'param': param},
                    'callback': self.parse,
                    'params': None
                }
        # 翻页
        yield self.request_next_page(baseItem, page, request_params)
        

