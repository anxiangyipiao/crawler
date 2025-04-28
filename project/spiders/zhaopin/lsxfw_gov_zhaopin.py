
from baseSpider.baseSpider import BaseSpiderObject,RequestItem
from urllib.parse import urljoin



class Shandong_JiNan_ggzy_jianshegongcheng_zhaobiao(BaseSpiderObject):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "lsxfw_gov_zhaopin"
    start_urls = 'https://www.lsxfw.cn/2020/news_list.php?cid=117'
       
    next_base_urls = 'http://web.nbdj.gov.cn/info_more.asp?newstype_id=436&CurPage={page}'
    contents_base_urls = ''  # 用于拼接详情页网址
    province = "浙江省"  # 必填，爬虫省份
    city = "丽水"  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '丽水先锋网'
    source = 'www.lsxfw.cn'

    timeRange = 7

    detail_xpath = '//div[@class="news_box"]'


    def start_requests(self):

            request_params = {
                'url': self.start_urls,
                'method': 'GET',
                'meta': {'page': 1},
                'callback': self.parse,
                'params': None
            }
            yield self.parse_task(RequestItem(**request_params))

    def parse(self, response):
        
        page = response.meta['page']

        node_list  = response.xpath('//ul[@class="List_box"]/li')
 
        for node in node_list:

            baseItem = self.get_base_item()
            baseItem['title'] = node.xpath('./a/text()').extract_first().strip()
            baseItem['publish_time'] =self.format_time_to_str(node.xpath('./p/text()').extract_first().strip())
            baseItem['url'] = urljoin(response.url,node.xpath('./a/@href').extract_first().strip())
   
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
                    'url': self.next_base_urls.format(page=page),
                    'method': 'GET',
                    'meta': {'page': page},
                    'callback': self.parse,
                    'params': None
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

    #         # 提取详情页的xpath
    #         xpath = '//div[@class="news_box"]'

    #         # 提取文本内容
    #         item = self.parse_contents_with_xpath(response, item, xpath)

    #         return item


    #     except Exception as e:

    #         return None