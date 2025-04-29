import random
import time
from baseSpider.baseSpider import BaseSpiderObject,RequestItem
from urllib.parse import urljoin
import requests
from scrapy.selector import Selector # 导入 Selector



class Shandong_JiNan_ggzy_jianshegongcheng_zhaobiao(BaseSpiderObject):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "tjrc_zhaopin"
    start_urls = 'https://www.tjrc.com.cn/app/article/newArticleAction!getzxList.do'
    next_base_urls = ''
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

                # WebList.aspx?id=
                id = node['zx_link'].strip().split('=')[1]

                baseItem['url'] = self.post_list(id)
                    

            else:

                baseItem['url'] = node['zx_link'].strip()
            
            print(baseItem['url'])

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


    def post_list(self, id):
        """
        发送POST请求
        """
        post_url = 'https://zxbm.tjtalents.com.cn/wsbm_ggfb//beifang/BeifangHdl.ashx'

        # 使用自定义请求头
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "connection": "keep-alive",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "ASP.NET_SessionId=31vdptzh10j21wed5zdxsrc0",
            "host": "zxbm.tjtalents.com.cn",
            "origin": "https://zxbm.tjtalents.com.cn",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        post_data = {
                "fun": "GetGgList",
                "id": id,
                "pagesize": "10",
                "page": "1"
        } 


        time.sleep(random.uniform(1, 3))
        res = requests.post(post_url, data=post_data, headers=headers)
       
        if res.status_code == 200:

            selector = Selector(text=res.text)

            url  = 'https://zxbm.tjtalents.com.cn/wsbm_ggfb//beifang/'+  selector.xpath('//div[@class="table_item"]/@onclick').extract_first().strip().split('\'')[1]

            return url





