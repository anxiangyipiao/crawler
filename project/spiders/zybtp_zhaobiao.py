
from baseSpider.baseSpider import BaseSpiderObject, RequestItem

# 建设工程
class Shandong_JiNan_ggzy_jianshegongcheng_zhaobiao(BaseSpiderObject):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "zybtp_zhaobiao"
    start_urls = [
        'https://www.zybtp.com/gcggg/index_{page}.jhtml',
        # 'https://www.zybtp.com/hcggg/index_{page}.jhtml',
    ]
    
    contents_base_urls = ''  # 用于拼接详情页网址

    province = "山东省"  # 必填，爬虫省份
    city = "济南市"  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '中原招标投标网'
    source = 'www.zybtp.com'


    def start_requests(self):

        for url in self.start_urls:

            urls = url.format(page=1)
            
            request_params = {
                'url': urls,
                'method': 'GET',
                'meta': {'page': 1, 'param': url},
                'callback': self.parse,
                'params': None
            }
            yield self.parse_task(RequestItem(**request_params))

    def parse(self, response):
        
        page = response.meta['page']
        param = response.meta['param']

        node_list  = response.xpath('//div[@class="List2 Top5"]/ul/li')
 
        for node in node_list:

            baseItem = self.get_base_item()
            baseItem['title'] = node.xpath('./a/text()').extract_first().strip()
            baseItem['publish_time'] = node.xpath('./p/span[5]/text()').extract_first().strip().split('：')[1][:10]
            baseItem['url'] = self.contents_base_urls + node.xpath('./a/@href').extract_first().strip()
   
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
        self.request_next_page(baseItem, page, request_params)
             
