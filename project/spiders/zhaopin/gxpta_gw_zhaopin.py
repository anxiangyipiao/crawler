
from baseSpider.baseSpider import BaseSpiderObject,RequestItem
from urllib.parse import urljoin

class Shandong_JiNan_ggzy_jianshegongcheng_zhaobiao(BaseSpiderObject):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "gxpta_gw_zhaopin"
    start_urls = 'https://www.gxpta.com.cn/ksxm/gwylxks/gxzzzzqzsjg2025ndgklxgwyzt/2025nzslxtztg/index.html'
    next_base_urls = 'https://www.gxpta.com.cn/ksxm/{type}/index_{page}.html'
    contents_base_urls = ''  # 用于拼接详情页网址
    province = "广西"  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '广西人事考试网'


    # https://www.gxpta.com.cn/ksxm/gwyzlks/gx2025ndkslygwyxdszt/2025ngwygg/
    # https://www.gxpta.com.cn/ksxm/gwylxks/gxzzzzqzsjg2025ndgklxgwyzt/2025nzslxtztg/index.html


    timeRange = 7
    max_page = 1

    detail_xpath = '//div[@class="article"]'

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


    lis = ['sydwzpks']

    
    def start_requests(self):

        for type in self.lis:

            request_params = {
                'url': self.start_urls,
                'method': 'GET',
                'meta': {'page': 1, 'type': type},
                'callback': self.parse,
                'params': None,
                'headers':self.headers,
            }
            yield self.parse_task(RequestItem(**request_params))

    
    def parse(self, response):
        
        page = response.meta['page']

        node_list  = response.xpath('//div[@class="rightitem"]/ul/li')
 
        for node in node_list:

            baseItem = self.get_base_item()
            baseItem['title'] = node.xpath('./a/@title').extract_first().strip()
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



