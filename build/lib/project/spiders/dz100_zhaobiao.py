import time
from baseSpider.baseSpider import BaseSpiderObject,RequestItem

class Henan_Pindingshan_ggzy_zhaobiaoSpider(BaseSpiderObject):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "dz100_zhaobiao"
    start_urls = [
         'https://api.dz100.com/bid/bidding/info/home/findProcurementNotice?pageNum={page}&pageSize=10'
    ]
    
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = '  https://api.dz100.com/bid/bidding/info/home/detail?id={id}'  # 用于拼接详情页网址
    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '大众招标网'
    source = 'dz100.com'

    def start_requests(self):

        for url in self.start_urls:
            
            time.sleep(1)
            urls = url.format(page = 1)
            
            # 设置请求参数
            request_params = {
                'request_body': None,
                'url': urls,
                'method': 'GET',
                'meta': {'page': 1, 'param': url},
                'callback': self.parse,
                'cookies': None,
                'headers': None,
                'params': None
            }

            yield self.parse_task(RequestItem(**request_params))

    def parse(self, response):
        
        param = response.meta['param']
        page = response.meta['page']

        node_list  =  response.json()['data']['list']
       
        for node in node_list:

            baseItem = self.get_base_item()
            baseItem['title'] = node['name']
            baseItem['publish_time'] = node['proStartTime'][:10]

            if node['proUrl'] != None and node['proUrl'] != '':
                baseItem['url'] = node['proUrl']
            else:
                baseItem['url'] = self.contents_base_urls.format(id=node['id'])
            
            baseItem['origin_url'] = 'https://www.dz100.com/gat/gateway/bidHall-info?id={id}'.format(id=node['id'])

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
        

