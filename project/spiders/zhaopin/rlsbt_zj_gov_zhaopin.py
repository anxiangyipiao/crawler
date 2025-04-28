
from baseSpider.baseSpider import BaseSpiderObject,RequestItem
from urllib.parse import urljoin
import re
from scrapy.selector import Selector # 导入 Selector

class Shandong_JiNan_ggzy_jianshegongcheng_zhaobiao(BaseSpiderObject):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "rlsbt_zj_gov_zhaopin"
    start_urls = 'https://rlsbt.zj.gov.cn/col/{type}/index.html?uid=7382343&pageNum=1'
    
    next_base_urls = 'https://rlsbt.zj.gov.cn/col/{type}/index.html?uid=7382343&pageNum={page}'
    contents_base_urls = ''  # 用于拼接详情页网址
    province = "浙江省"  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '浙江省人力资源和社会保障厅'
    source = 'rlsbt.zj.gov.cn'

    timeRange = 7
    detail_xpath = '//div[@class="contant"]'

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
    }


    lis = ['col1229743683','col1229116948']

    
    def start_requests(self):

        for type in self.lis:

            request_params = {
                'url': self.start_urls.format(type=type),
                'method': 'GET',
                'meta': {'page': 1, 'type': type},
                'callback': self.parse,
                'params': None,
                'headers':self.headers,
            }
            yield self.parse_task(RequestItem(**request_params))

    
    def extracr_node_list(self, response):

        text = re.search(r'<recordset>(.*)</recordset>', response.text, re.DOTALL | re.IGNORECASE).group(1).strip()

        # <record><![CDATA[ , ]]></record> 去除
        text = text.replace('<record><![CDATA[','').replace(']]></record>','')

        selector = Selector(text=text)

        # 提取所有的 <li> 节点
        node_list = selector.xpath('//li')

        return node_list


    def parse(self, response):
        
        page = response.meta['page']

        # 提取数据
        node_list = self.extracr_node_list(response)

        for node in node_list:

            baseItem = self.get_base_item()
            baseItem['title'] = node.xpath('.//a/@title').extract_first().strip()
            baseItem['publish_time'] = self.format_time_to_str(node.xpath('.//span[@class="bt_time"]/text()').extract_first().strip())
            baseItem['url'] = urljoin(response.url,node.xpath('.//a/@href').extract_first().strip())
   
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

    # def parse_html(self,response,item):
    #     """
    #     解析HTML响应并填充item对象。
        
    #     Args:
    #         response (Response): Scrapy的Response对象，包含网页的响应内容。
    #         item (BaseItem): 需要填充数据的item对象。
        
    #     Returns:
    #         BaseItem: 填充了网页内容的item对象。
        
    #     """
        
    #     try:

    #          # 提取详情页的xpath
    #         xpath = '//div[@class="contant"]'

    #         # 提取文本内容
    #         item = self.parse_contents_with_xpath(response, item, xpath)

    #         return item


    #     except Exception as e:

    #         return None