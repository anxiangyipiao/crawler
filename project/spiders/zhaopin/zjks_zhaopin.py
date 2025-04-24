
from baseSpider.baseSpider import BaseSpiderObject,RequestItem
from urllib.parse import urljoin



class Shandong_JiNan_ggzy_jianshegongcheng_zhaobiao(BaseSpiderObject):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "zjks_zhaopin"
    start_urls = 'http://gwy.zjks.com/zjgwy/website/queryMore.htm'
    next_base_urls = 'http://www.spic.com.cn/2021/jrwm/index_{page}.html#pages'
    contents_base_urls = ''  # 用于拼接详情页网址
    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '浙江省公务员考试录用网'
    source = 'gwy.zjks.com'

    timeRange = 7
    max_page = 1


    params = {
        "mkxh": "2",
        "oldornew": "new",
        "dsdm": "133"
    }

    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "DNT": "1",
        "Host": "gwy.zjks.com",
        "Origin": "http://gwy.zjks.com",
        "Pragma": "no-cache",
        "Referer": "http://gwy.zjks.com/zjgwy/website/init.htm",
        "Upgrade-Insecure-Requests": "1"
    }


    dsdms = [
            '133','13301','13302','13303','13304','13305','13306','13307','13308','13309','13310','13311'
            ]


    def start_requests(self):

        for dsdm in self.dsdms:

            self.params['dsdm'] = dsdm
           
            request_params = {
                'url': self.start_urls,
                'method': 'POST',
                'meta': {'page': 1,'dsdm': dsdm},
                'callback': self.parse,
                'params': self.params,
                'request_body': 'formdata',
                'headers': self.header,
            }
            yield self.parse_task(RequestItem(**request_params))

    def parse(self, response):
        
        page = response.meta['page']
        dsdm = response.meta['dsdm']

        node_list  = response.xpath('//div[@class="ibox-content"]//tbody/tr')

        for node in node_list:

            baseItem = self.get_base_item()
            baseItem['title'] = node.xpath('.//a/text()').extract_first().strip()
            baseItem['publish_time'] = node.xpath('./td[2]/text()').extract_first().strip()


            mkxh = node.xpath('.//a/@onclick').extract_first().strip().split('\'')[1]
            tzid = node.xpath('.//a/@onclick').extract_first().strip().split('\'')[3]

            baseItem['url'] = node.xpath('.//a/@onclick').extract_first().strip()
   
            request_params = {
                    'url': 'http://gwy.zjks.com/zjgwy/website/queryDetail.htm',
                    'meta': {'item': baseItem},
                    'callback': self.parse_content_detal,
                    'errback': self.errback_httpbin,
                    'request_body': 'formdata',
                    'method': 'POST',
                    'headers': self.header,
                    'params': {
                        'mkxh': mkxh,
                        'oldornew': 'new',
                        'dsdm': dsdm,
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

            # 提取文本内容
            text_content = ''.join(response.xpath('//div[@class="ibox float-e-margins"]//text()').getall()).strip()

           # 提取附件链接
            attachment_links = response.xpath('//div[@class="ibox float-e-margins"]//a/@href').getall()

            if  attachment_links.startwith('http'):
                # 如果链接是完整的，则直接使用
                full_attachment_links = attachment_links

            else:
                # 将相对路径转换为完整的 URL
                full_attachment_links = [urljoin(response.url, link) for link in attachment_links]

            # 将文本内容和附件链接组合
            item['contents'] = {
                'text': text_content,
                'attachments': full_attachment_links
            }
                     
            return item

        except Exception as e:

            return None