
from baseSpider.baseSpider import BaseSpiderObject,RequestItem
from urllib.parse import urljoin
import re

class Shandong_JiNan_ggzy_jianshegongcheng_zhaobiao(BaseSpiderObject):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "mohrss_zhaopin"
    start_urls = 'https://www.mohrss.gov.cn/SYrlzyhshbzb/fwyd/SYkaoshizhaopin/zyhgjjgsydwgkzp/{type}/index.html'
    next_base_urls = 'https://www.mohrss.gov.cn/SYrlzyhshbzb/fwyd/SYkaoshizhaopin/zyhgjjgsydwgkzp/{type}/index_{page}.html'
    contents_base_urls = ''  # 用于拼接详情页网址
    province = "国家"  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '中华人民共和国人力资源和社会保障部'
    source = 'www.mohrss.gov.cn'

    timeRange = 7
    max_page = 1

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cache-control': 'no-cache',
        'host': 'www.mohrss.gov.cn',
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


    lis = ['zpgg', 'gxbyszpzl', 'zytz']

    def generate_cookies(self,WTKkN,bOYDu,wyeCN,increment):

        tst_status = WTKkN + bOYDu + wyeCN

        EO_Bot_Ssid = increment

        return {
            "__tst_status": f"{tst_status}#",
            "EO_Bot_Ssid": EO_Bot_Ssid
        }

    def extract_variables(self,javascript_code):
        """
        从 JavaScript 代码中提取变量值
        """

        match_wtkkn = re.search(r"WTKkN\s*:\s*(\d+)", javascript_code).group(1)
        # 查找 bOYDu: 后面的数字
        match_boydu = re.search(r"bOYDu\s*:\s*(\d+)", javascript_code).group(1)
        # 查找 wyeCN: 后面的数字
        match_wyecn = re.search(r"wyeCN\s*:\s*(\d+)", javascript_code).group(1)

        # 提取 EO_Bot_Ssid 增量值
        regex = r'case\s*"3":.*?\(t,\s*(\d+)\s*\);'
        match = re.search(regex, javascript_code, re.DOTALL).group(1)

        # 返回提取的变量值
        return int(match_wtkkn), int(match_boydu), int(match_wyecn), int(match)
  
    def start_requests(self):

        for type in self.lis:

            request_params = {
                'url': self.start_urls.format(type=type),
                'method': 'GET',
                'meta': {'page': 0, 'type': type},
                'callback': self.parse_cookies,
                'params': None,
                'headers':self.headers,
            }
            yield self.parse_task(RequestItem(**request_params))

    def parse_cookies(self, response):

        # 提取变量值
        wtkkn, bOYDu, wyeCN, increment = self.extract_variables(response.text)

        # 生成 cookies
        cookies = self.generate_cookies(
            WTKkN=wtkkn,
            bOYDu=bOYDu,
            wyeCN=wyeCN,
            increment=increment
        )


        request_params = {
                'url': response.url,
                'method': 'GET',
                'meta': response.meta,
                'callback': self.parse,
                'params': None,
                'headers':self.headers,
                'cookies': cookies,
            }
        
        
        yield self.parse_task(RequestItem(**request_params))

    def parse(self, response):
        
        page = response.meta['page']

        node_list  = response.xpath('//ul[@class="rsb_ej_zpggList"]/li')
 
        for node in node_list:

            baseItem = self.get_base_item()
            baseItem['title'] = node.xpath('.//a/text()').extract_first().strip()
            baseItem['publish_time'] =self.format_time_to_str(node.xpath('.//span/text()').extract_first().strip())
            baseItem['url'] = urljoin(response.url,node.xpath('./a/@href').extract_first().strip())
   
            request_params = {
                    'url': baseItem['url'],
                    'meta': {'item': baseItem},
                    'callback': self.parse_content_detal,
                    'errback': self.errback_httpbin,
                    'headers':self.headers,
                    'cookies': response.request.cookies,
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
                    'cookies': response.request.cookies,
                }
        # 翻页
        yield self.request_next_page(baseItem, page, request_params)

    def parse_html(self,response,item):
        """
        解析HTML响应并填充item对象。
        
        Args:
            response (Response): Scrapy的Response对象，包含网页的响应内容。
            item (BaseItem): 需要填充数据的item对象。
        
        Returns:
            BaseItem: 填充了网页内容的item对象。
        
        """
        
        try:

             # 提取详情页的xpath
            xpath = '//div[@class="rsb_ejDetail_cont"]'

            # 提取文本内容
            item = self.parse_contents_with_xpath(response, item, xpath)

            return item


        except Exception as e:

            return None