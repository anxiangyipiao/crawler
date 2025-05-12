import datetime
import json
import random
import re
import time
from urllib.parse import urljoin
import scrapy
# -------------------------------tag-------------------------------------------
# 这里需要在python安装目录\Lib\site-packages下创建 .pth文件，内容为sp_control.py的路径
from sp_action.sp_control import ZhaotoubiaoBaseSpider
from sp_action.items import SpiderItem
from lxml import etree
import urllib


class template_zhaobiao(ZhaotoubiaoBaseSpider):
    # ggzy: 公共资源网     zfcg：政府采购
    name = "jzsz_edu_cn_zhaobiao"
    start_urls = [
       "https://www.jzsz.edu.cn/zbgs/list.htm",  # 招标信息列表页
    ]
    
    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = ''  # 用于拼接详情页网址
    page_urls = ""  # 用于获取下一页网址

    province = ""  # 必填，爬虫省份
    city = ""  # 必填，爬虫城市
    county = ""  # 选填，爬虫区/县
    site_name = "焦作师范高等专科"  # 必填，爬虫网站名称
    source = start_urls[0].split('/')[2]
    max_page = 1

    headers = {
         'User-Agent':  "Mozilla/5.0 (Linux; Android 14; Xiaomi 13 Build/UP1A.230905.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.170 Mobile Safari/537.36",
    }
 
    def start_requests(self):

        for url in self.start_urls:

            yield scrapy.Request(url,method='get',callback=self.parse,dont_filter=True,meta={'page':1},headers=self.headers)

    def parse(self, response):
        
        page = response.meta['page']

        node_list  = response.xpath("//div[@class='column-news-list clearfix']//ul[@class='wp_article_list']//li")
 
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
  
    def extract_title_url_info(self, title_element):
        """
        从标题元素中提取标题和URL。
        
        Args:
            title_element (list): 标题元素列表
            
        Returns:
            tuple: (标题, URL)或(None, None) 如果发生错误
        """
        if title_element is None or len(title_element) == 0:
            return None, None
        
        try:
            if len(title_element) == 1:
                title_attr = title_element[0].get("title")
                url = title_element[0].get("href")

                if title_attr and title_attr.strip():

                    return title_attr.strip(), url
                
                else:
                    # 如果没有title属性或title为空，则使用元素文本内容

                    return title_element[0].xpath("string(.)"), url
                
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
                        longest_url = element.get("href")
          
                return longest_text, longest_url
                
        except Exception as e:
          
            return None, None

    def extract_date_info(self, element):

        DATE_PATTERN = re.compile(r"\d{4}[-/.年]\d{2}[-/.月]\d{2}[日]?")

       # 尝试提取日期
        date_text = element.xpath("string(.)").strip()
        date_match = DATE_PATTERN.search(date_text)
            
        if date_match:
            raw_date = date_match.group(0)
                # 标准化日期格式为yyyy-MM-dd
            clean_date = raw_date.replace("年", "-").replace("月", "-").replace("日", "").replace("/", "-").replace(".", "-")
                # 处理可能的多余空格和时间部分
            clean_date = re.sub(r'\s+.*$', '', clean_date)  # 移除时间部分

            return clean_date

    def extract_a_label_info(self, element):
        '''
        提取a标签的标题和URL信息。
        '''

        url = element.get("href",None)

        if element.get("title",None):
            title = element.get("title")
        else:
            title = element.xpath("string(.)").strip()

        return title, url

    def extract_item_info(self, element, res_url):
        """
        从列表项元素中提取信息。
        
        Args:
            element: HTML元素
            res_url (str): 响应URL
            
        Returns:
            dict: 包含提取信息的字典或None如果发生错误
        """
            
        from lxml import etree

        # 使用XPath解析HTML元素
        element = etree.HTML(element.extract())


        try:
            # 创建一个字典来存储提取的信息
            item = {}

            # 如果本身就是a标签，直接提取
            if element.tag == "a":
                
                item["title"], item["url"] = self.extract_a_label_info(element)
                if item["url"]:
                    item["url"] = urljoin(res_url, item["url"])

            else:
              
                # 尝试提取标题 - 通常在a标签内
                title_url_element = element.xpath(".//a")
                
                if title_url_element:
                    item["title"], item["url"] = self.extract_title_url_info(title_url_element)
                    if item["url"]:
                        item["url"] = urljoin(res_url, item["url"])  # 处理相对链接

            # 去掉多余的空格
            if item.get("title") and item.get("url"):
                item["title"] = re.sub(r'\s+', ' ', item["title"]).strip()
                decoded_url = urllib.parse.unquote(item.get("url"))
                url = re.sub(r'\s+', '', decoded_url)
                item["url"] = url
            
        
            item["date"] = self.extract_date_info(element)
            if not item["date"]:
                item["date"] = None
            
            return item
            
        except Exception as e:
         
            return None