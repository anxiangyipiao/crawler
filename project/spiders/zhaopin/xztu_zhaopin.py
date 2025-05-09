
from baseSpider.baseSpider import BaseSpiderObject,RequestItem
from urllib.parse import urljoin
import re

class Shandong_JiNan_ggzy_jianshegongcheng_zhaobiao(BaseSpiderObject):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "xztu_zhaopin"
    start_urls = 'http://www.xztu.edu.cn/index/{type}.htm'
    next_base_urls = 'https://www.dtdjzx.gov.cn/{type}/index_{page}.jhtml'
    contents_base_urls = ''  # 用于拼接详情页网址
    province = "山东省"  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '忻州师范学院'
 

    timeRange = 7
    max_page = 1
    use_mobile_ua = True
    

    detail_xpath = '//div[@class="content-box"]'



    lis = ['tzgg']

    
    def start_requests(self):

        for type in self.lis:

            request_params = {
                'url': self.start_urls.format(type=type),
                'method': 'GET',
                'meta': {'page': 1, 'type': type},
                'callback': self.parse,
                'params': None,
            }
            yield self.parse_task(RequestItem(**request_params))

    
    def parse(self, response):
        
        page = response.meta['page']

        node_list  = response.xpath("//ul/li[@class='list-item']")
 
        for node in node_list:

            baseItem = self.get_base_item()

            title,url = self.auto_extract_url_title(node,response.url)

            print('title:',title)
            print('url:',url)

            baseItem['title'] = node.xpath('.//a/@title').extract_first().strip()
            baseItem['publish_time'] = self.format_time_to_str(node.xpath('.//span/text()').extract_first().strip())
            baseItem['url'] = urljoin(response.url,node.xpath('./a/@href').extract_first().strip())
   
            request_params = {
                    'url': baseItem['url'],
                    'meta': {'item': baseItem},
                    'callback': self.parse_content_detal,
                    'errback': self.errback_httpbin,
                    'headers':self.headers,
                }

             # 判断是否继续爬取
            if self.calculate_task_item(baseItem):

                # 爬取详情页
                yield self.parse_task(RequestItem(**request_params))
         
 
        # 翻页,需要构建新的请求参数
        page += 1
        request_params = {
                    'url': self.next_base_urls.format(page=page,type=response.meta['type']),
                    'method': 'GET',
                    'meta': {'page': page, 'type': response.meta['type']},
                    'callback': self.parse,
                    'params': None,
                    'headers':self.headers,
                }
        # 翻页
        yield self.request_next_page(baseItem, page, request_params)



