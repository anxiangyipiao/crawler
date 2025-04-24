
from baseSpider.baseSpider import BaseSpiderObject,RequestItem
from urllib.parse import urljoin



class Shandong_JiNan_ggzy_jianshegongcheng_zhaobiao(BaseSpiderObject):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "csjgwy_zhaopin"
    start_urls = 'http://www.csjgwy.com/tyzpwb/website/queryMore.htm'
    next_base_urls = 'http://www.spic.com.cn/2021/jrwm/index_{page}.html#pages'
    contents_base_urls = ''  # 用于拼接详情页网址
    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '长三角'
    source = 'www.csjgwy.com'

    timeRange = 7
    max_page = 1


    params = {
        "mkxh": "2",
        "dsdm": ""
    }

    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "DNT": "1",
        "Host": "www.csjgwy.com",
        "Origin": "http://www.csjgwy.com",
        "Pragma": "no-cache",
        "Referer": "http://www.csjgwy.com/tyzpwb/website/init.htm",
        "Upgrade-Insecure-Requests": "1"
    }


    def start_requests(self):

            request_params = {
                'url': self.start_urls,
                'method': 'POST',
                'meta': {'page': 1},
                'callback': self.parse,
                'params': self.params,
                'request_body': 'formdata',
                'headers': self.header,
            }
            yield self.parse_task(RequestItem(**request_params))

    def parse(self, response):
        
        page = response.meta['page']

        node_list_item  = response.xpath('//div[@class="newslistbox"]/div[@class="newsinfo"]')
        node_list_time  = response.xpath('//div[@class="newslistbox"]/div[@class="newstime"]')

        for index, node in enumerate(node_list_item):

            baseItem = self.get_base_item()
            baseItem['title'] = node.xpath('.//a/text()').extract_first().strip()
            baseItem['publish_time'] = node_list_time[index].xpath('./text()').extract_first().strip()


            tzid = node.xpath('.//a/@onclick').extract_first().strip().split('\'')[1]

            baseItem['url'] = node.xpath('.//a/@onclick').extract_first().strip()
   
            request_params = {
                    'url': 'http://www.csjgwy.com/tyzpwb/website/queryDetail.htm',
                    'meta': {'item': baseItem},
                    'callback': self.parse_content_detal,
                    'errback': self.errback_httpbin,
                    'request_body': 'formdata',
                    'method': 'POST',
                    'headers': self.header,
                    'params': {
                        'mkxh': '2',
                        'dsdm': '',
                        'tzid': tzid,
                    }

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
            xpath = 'div[@class="newslistbox"]'

            # 提取文本内容
            item = self.parse_contents_with_xpath(response, item, xpath)

            return item

        

        except Exception as e:

            return None