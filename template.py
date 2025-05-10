import datetime
import json
import random
import re
import time
import scrapy
# -------------------------------tag-------------------------------------------
# 这里需要在python安装目录\Lib\site-packages下创建 .pth文件，内容为sp_control.py的路径
from sp_action.sp_control import ZhaotoubiaoBaseSpider
from sp_action.items import SpiderItem
from lxml import etree
import urllib


class template_zhaobiao(ZhaotoubiaoBaseSpider):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "{name}"
    start_urls = [
       "{url}",  # 招标信息列表页
    ]
    
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = ''  # 用于拼接详情页网址
    page_urls = ""  # 用于获取下一页网址

    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = "{site_name}"  # 必填，爬虫网站名称
    source = start_urls[0].split('/')[2]
    max_page = 1

    headers = {
         'User-Agent':  "{user_agent}",
    }
 
    def start_requests(self):

        for url in self.start_urls:

            yield scrapy.Request(url,method='get',callback=self.parse,dont_filter=True,meta={'page':1},headers=self.headers)

    def parse(self, response):
        
        page = response.meta['page']

        node_list  = response.xpath("{list_xpath}")
 
        for node in node_list:

            # 如果a标签不node存在，则跳过
            if not node.xpath(".//a"):
                continue
            item = SpiderItem()
            item['source'] = self.source
            item['site_name'] = self.site_name
            item['province'] = self.province
            item['city'] = self.city
            item['county'] = self.county

            temp_item = self.extract_item_info(node, response.url)

            print("temp_item:%s" % temp_item)

            item['title'] = temp_item['title']
            item['publish_time'] = temp_item['date']
            item['url'] = temp_item['url']
            # -------------------------------tag-------------------------------------------
            add_task = self.add_download_task(item['url'],item['publish_time'])
            # 招标内容
            if add_task == False:
                time.sleep(random.randint(1, 3))
                yield scrapy.Request(item['url'], callback=self.parse_detail,
                                      meta={'item': item},headers=self.headers
                                      )
        # -------------------------------tag-------------------------------------------
        # 检查当页数据日期，判断是否翻页
        if node_list != None and len(node_list) > 0:
            check_publish_time = self.check_published_time(item['publish_time'])
            # print("check_publish_time:%s" % check_publish_time)
        # -------------------------------tag-------------------------------------------
        # if self.pagecount < int(self.max_page) and check_publish_time:
        if page < int(self.max_page) and check_publish_time:
           pass
        else:
            # -------------------------------tag-------------------------------------------
            # 标记翻页结束
            self.page_over = True

    def parse_detail(self, response):
        # 获取详情页数据
        item = response.meta['item']
        item['contents'] = response.text
        yield item
  
    def extract_item_info(self, node, res_url):
        """从列表项元素中提取标题、日期和链接等信息"""

        from lxml import etree

        # 使用XPath解析HTML元素
        element = etree.HTML(node.extract())


        # 创建一个字典来存储提取的信息
        item = {}
        
        # 尝试提取标题 - 通常在a标签内
        title_url_element = element.xpath(".//a")
        
        if title_url_element:
           
            item["title"],item["url"] = self.extract_title_url_info(title_url_element)
            item["url"] = urllib.parse.urljoin(res_url, item["url"])  # 处理相对链接
        
        
        # 尝试提取日期 2021-05-11 使用regex匹配
        date_element = element.xpath(".//text()")
        date_text = "".join(date_element).strip()
        date_match = re.search(r"\d{4}[-/.年]\d{2}[-/.月]\d{2}", date_text)
        if date_match:
            item["date"] = date_match.group(0).replace("年", "-").replace("月", "-").replace("日", "").replace("/", "-").replace(".", "-")
        else:
            item["date"] = None

        
        return item

    def extract_title_url_info(self, title_element):

        if title_element is None:
            return None
        
        if len(title_element) == 1:

            title_attr = title_element[0].get("title")
            if title_attr and title_attr.strip():

                title = re.sub(r'\s+', '', title_attr.strip())

                return title,title_element[0].get("href")
            else:
                # 如果没有title属性或title为空，则使用元素文本内容
                title = re.sub(r'\s+', '', title_element[0].xpath("string(.)").strip())
                return title,title_element[0].get("href")
                
            
        if len(title_element) > 1:
            # 如果有多个元素，返回最长元素的文本内容及其URL
            longest_text = ""
            longest_url = ""
            for element in title_element:
                if element.get("title") and element.get("title").strip():
                    text = element.get("title").strip()
                else:
                    text = element.xpath("string(.)").strip()
                
                # 当找到更长的文本时，同时保存其URL
                if len(text) > len(longest_text):
                    longest_text = text
                    longest_url = element.get("href")  # 获取当前最长文本对应的URL
            
            # re 去掉空格
            longest_text = re.sub(r'\s+', '', longest_text)

            return longest_text, longest_url  # 返回最长文本和对应的URL