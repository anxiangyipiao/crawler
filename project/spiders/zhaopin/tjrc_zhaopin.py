
from baseSpider.baseSpider import BaseSpiderObject,RequestItem
from urllib.parse import urljoin
import requests
from scrapy.selector import Selector # 导入 Selector



class Shandong_JiNan_ggzy_jianshegongcheng_zhaobiao(BaseSpiderObject):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "tjrc_zhaopin"
    start_urls = 'https://www.tjrc.com.cn/app/article/newArticleAction!getzxList.do'
    next_base_urls = 'http://www.spic.com.cn/2021/jrwm/index_{page}.html#pages'
    contents_base_urls = ''  # 用于拼接详情页网址
    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = '中国北方人才市场'
    source = 'www.tjrc.com.cn'

    timeRange = 7
    detail_xpath = 'div[@class="article-body"]'

    params = {
        "currentPage": "1",
        "cate_id": "3013",
        "searchstr": ""
    }

    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
        "DNT": "1",
        "Host": "www.tjrc.com.cn",
        "Origin": "https://www.tjrc.com.cn",
        "Pragma": "no-cache",
        "Referer": "https://www.tjrc.com.cn/app/article/list/3013.shtml",
        "Upgrade-Insecure-Requests": "1"
    }

    dsdms = [
            '3013'
            ]


    def start_requests(self):

        for dsdm in self.dsdms:

            self.params['cate_id'] = dsdm
           
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

        node_list  = response.json()['articlelist']

        for node in node_list:

            baseItem = self.get_base_item()
            baseItem['title'] = node['zxmc'].strip()
            baseItem['publish_time'] =self.format_time_to_str(node['pxtj'].strip())


            if 'WebList' in node['zx_link'].strip():

                res = requests.get(node['zx_link'].strip(),headers=self.header)

                if res.status_code == 200:

                    selector = Selector(text=res.text)
                    baseItem['url'] = 'https://zxbm.tjtalents.com.cn/wsbm_ggfb//beifang/'+  selector.xpath('//div[@id="tzggdiv"]/div[1]/@onclick').extract_first().strip().split('\'')[1]

            else:

                baseItem['url'] = node['zx_link'].strip()
            
 
            request_params = {
                        'url': baseItem['url'],
                        'meta': {'item': baseItem},
                        'callback': self.parse_content_detal,
                        'errback': self.errback_httpbin,
                        'method': 'GET',
                        'headers': self.header,
                    }

                # 判断是否继续爬取
            if self.calculate_task_item(baseItem):

                    # 爬取详情页
                yield self.parse_task(RequestItem(**request_params))
         
 
        # 翻页,需要构建新的请求参数
        page += 1
        self.params['currentPage'] = str(page)
        self.params['cate_id'] = dsdm
        request_params = {
                    'url': self.start_urls,
                    'method': 'POST',
                    'meta': {'page': page,'dsdm': dsdm},
                    'callback': self.parse,
                    'params': self.params,
                    'request_body': 'formdata',
                    'headers': self.header,
                }
        # 翻页
        yield self.request_next_page(baseItem, page, request_params)










