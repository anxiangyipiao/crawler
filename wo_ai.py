import json
import re
import requests
import random
import os
import urllib
import logging
import time
from urllib.parse import urljoin
from lxml import etree

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("WoCloudAI")

# 预编译正则表达式提高性能
BODY_PATTERN = re.compile(r"<body.*?>(.*?)</body>", re.DOTALL)
SCRIPT_PATTERN = re.compile(r"<script.*?>.*?</script>", re.DOTALL)
STYLE_PATTERN = re.compile(r"<style.*?>.*?</style>", re.DOTALL)
IMG_PATTERN = re.compile(r"<img.*?>", re.DOTALL)
COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)
WHITESPACE_PATTERN = re.compile(r"\s+")
EMPTY_TAG_PATTERN = re.compile(r"<([a-zA-Z]+)[^>]*>[\s\n\r\t]*</\1>", re.DOTALL)
CHARSET_PATTERN = re.compile(r'charset=(\S+)')
DATE_PATTERN = re.compile(r"\d{4}[-/.年]\d{2}[-/.月]\d{2}[日]?")

# 从环境变量获取令牌或使用默认值
X_YP_ACCESS_TOKEN = "a36a90f6-d119-4b50-970f-30894a2f39fa"


class WoCloudAI:
    """沃云AI助手类，用于分析网页和提取招标公告列表。"""

    def __init__(self):
        """初始化WoCloudAI实例和相关配置。"""
        self.url = "https://panservice.mail.wo.cn/wohome/ai/assistant/query"
        self.x_yp_client_id = [
            "1001000035", "1001000036", "1001000037", "1001000021",
            "1001000022", "1001000023", "1001000024", "1001000025",
            "1001000026", "1001000027", "1001000028", "1001000029",
            "1001000030", "1001000031", "1001000032", "1001000033",
            "1001000034",
        ]
        self.user_agent = [
            "Mozilla/5.0 (Linux; Android 14; MEIZU 21 Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.64 Mobile Safari/537.36/woapp LianTongYunPan/3.0.14 (Android 14)",
            "Mozilla/5.0 (Linux; Android 13; Google Pixel 6 Build/TQ3A.230805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.170 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; Samsung Galaxy S21 Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/113.0.5672.92 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; OnePlus 9 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/112.0.5615.49 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 14; Xiaomi 13 Build/UP1A.230905.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.170 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; Huawei P40 Build/HUAWEIANA-LX4; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.77 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 9; Oppo Reno 3 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.124 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 8; Vivo X21 Build/O11019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.91 Mobile Safari/537.36",
        ]
        self.request_timeout = 30  # 请求超时时间(秒)
        self.max_retries = 3  # 最大重试次数
        self.retry_delay = 2  # 重试延迟(秒)
        self.ai_headers =  {
                "Host": "panservice.mail.wo.cn",
                "Connection": "close",
                "sec-ch-ua": '"Not)A;Brand";v="99", "Android WebView";v="127", "Chromium";v="127"',
                "X-YP-Access-Token": X_YP_ACCESS_TOKEN,
                "X-YP-App-Version": "3.0.14",
                "sec-ch-ua-mobile": "?1",
                "User-Agent": random.choice(self.user_agent),
                "Content-Type": "application/json",
                "accept": "text/event-stream",
                "X-YP-Client-Id": random.choice(self.x_yp_client_id),
                "sec-ch-ua-platform": '"Android"',
                "Origin": "https://panservice.mail.wo.cn",
                "X-Requested-With": "com.chinaunicom.bol.cloudapp",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://panservice.mail.wo.cn/h5/wocloud_ai/",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            }

    def _get_headers(self, is_mobile=True):
        """
        生成请求头。
        
        Args:
            is_mobile (bool): 是否使用移动设备的用户代理
            
        Returns:
            dict: 包含请求头信息的字典
        """
        if is_mobile:

            headers = {
                "User-Agent":   "Mozilla/5.0 (Linux; Android 14; Xiaomi 13 Build/UP1A.230905.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.170 Mobile Safari/537.36",
            }
        else:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            }
        
        return headers

    def query(self, input_text="", model_id=0, tag=0, history=None):
        """
        向AI模型发送查询请求。
        
        Args:
            input_text (str): 输入文本
            model_id (int): 模型ID，0是默认模型，1是deepseek
            tag (int): 标签
            history (list): 历史对话
            
        Returns:
            str: AI模型的响应，如果发生错误则返回None
        """

        data = {"input": input_text, "modelId": model_id, "tag": tag, "history": None}
        
        for attempt in range(self.max_retries):
            try:            
                response = requests.post(
                    self.url, 
                    headers=self.ai_headers, 
                    json=data, 
                    timeout=self.request_timeout
                )
                response.raise_for_status()

                full_response = ""
                for line in response.iter_lines():
                    decoded_line = line.decode("utf-8").replace("data:", "").strip()
                    if len(decoded_line) != 0:
                        try:
                            json_line = json.loads(decoded_line)
                            full_response += json_line.get("response", "")
                        except json.JSONDecodeError:
                            logger.warning(f"无法解析JSON行: {decoded_line}")
                
                if full_response:
                    logger.info("成功获取AI响应")
                    return full_response
                else:
                    logger.warning("收到空响应")
                    return None

            except requests.exceptions.RequestException as e:
                logger.error(f"请求失败: {str(e)}")
                if attempt < self.max_retries - 1:
                    logger.info(f"等待 {self.retry_delay}秒后重试...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error("达到最大重试次数，放弃请求")
                    return None
            except Exception as e:
                logger.error(f"处理响应时发生错误: {str(e)}")
                return None

    def _fetch_content(self, url, is_mobile=True):
        """
        获取URL的内容。
        
        Args:
            url (str): 要获取内容的URL
            is_mobile (bool): 是否使用移动设备的用户代理
            
        Returns:
            tuple: (清理后的HTML内容, 响应URL)或(None, None)如果发生错误
        """
            
        for attempt in range(self.max_retries):
            try:
                headers = self._get_headers(is_mobile=is_mobile)
              
                response = requests.get(url, headers=headers, timeout=self.request_timeout)
                response.raise_for_status()
                
                # 尝试从Content-Type头部获取正确的编码
                content_type = response.headers.get('Content-Type', '')
                encoding_match = CHARSET_PATTERN.search(content_type)
                
                if encoding_match:
                    encoding = encoding_match.group(1)
                else:
                    # 如果响应头没有指定编码，使用apparent_encoding
                    encoding = response.apparent_encoding
                
                # 显式设置响应的编码
                response.encoding = encoding
                
                # 清理响应内容
                cleaned_response = self.clean_response(response.text)
                
                return cleaned_response, response.url
                
            except requests.exceptions.RequestException as e:
                logger.error(f"获取内容失败: {str(e)}")
                if attempt < self.max_retries - 1:
                    logger.info(f"等待 {self.retry_delay}秒后重试...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error("达到最大重试次数，放弃请求")
                    return None, None
            except Exception as e:
                logger.error(f"处理内容时发生错误: {str(e)}")
                return None, None

    def get_content_with_window(self, url):
        """
        使用PC端用户代理获取URL内容。
        
        Args:
            url (str): 要获取内容的URL
            
        Returns:
            tuple: (清理后的HTML内容, 响应URL)
        """
        return self._fetch_content(url, is_mobile=False)

    def get_content_with_mobile(self, url):
        """
        使用移动端用户代理获取URL内容。
        
        Args:
            url (str): 要获取内容的URL
            
        Returns:
            tuple: (清理后的HTML内容, 响应URL)
        """
        return self._fetch_content(url, is_mobile=True)

    def clean_response(self, html_content):
        """
        清理HTML内容。
        
        Args:
            html_content (str): 原始HTML内容
            
        Returns:
            str: 清理后的HTML内容
        """
        if not html_content:
            return ""
            
        try:
            # 选取body部分
            body_match = BODY_PATTERN.search(html_content)
            if body_match:
                html_content = body_match.group(1)
            
            # 剔除不需要的部分
            html_content = SCRIPT_PATTERN.sub("", html_content)
            html_content = STYLE_PATTERN.sub("", html_content)
            html_content = IMG_PATTERN.sub("", html_content)
            html_content = COMMENT_PATTERN.sub("", html_content)
            html_content = WHITESPACE_PATTERN.sub(" ", html_content)
            html_content = EMPTY_TAG_PATTERN.sub("", html_content)
            
            return html_content
        except Exception as e:
            logger.error(f"清理HTML内容时发生错误: {str(e)}")
            return html_content  # 返回原始内容

    def get_prompt(self, contents):
        """
        生成提示文本。
        
        Args:
            contents (str): HTML内容
            
        Returns:
            str: 格式化的提示文本
        """
        if not contents:
            logger.warning("无内容用于生成提示")
            return ""
            
        prompt = """
            请分析HTML并提取招标公告列表的XPath表达式，遵循以下分析流程：

            步骤1：识别招标列表结构
            - 查找包含重复项的列表结构（如ul/li、table/tr、div组等）
            - 确定招标公告的特征：必须包含标题、日期、链接，且格式统一
            - 排除导航菜单、页脚链接等非招标内容的列表

            步骤2：构建精确XPath
            - 为找到的列表项创建XPath，确保选择整个列表项而非子元素
            - 优先使用id、class等特定属性进行定位
            - 确保XPath能选中所有目标列表项，不多不少

            步骤3：优化表达式
            - 确保XPath以//开头，便于在任何位置查找
            - 使用最简洁但有效的选择器（避免过长或过于复杂的表达式）
            - 验证XPath能否准确定位到列表项级别
            - 标签都是小写
            
            示例输出格式：//div[@class='news-list']//ul//li 
            
            分析此HTML并仅返回一个最准确的XPath表达式，无需解释：
            {text}
        """
        return prompt.format(text=contents)

    def get_res_by_xpath(self, xpath, content, res_url):
        """
        使用XPath从HTML内容中提取数据。
        
        Args:
            xpath (str): XPath表达式
            content (str): HTML内容
            res_url (str): 响应URL
            
        Returns:
            list: 提取的项目列表
        """
            
        try:
            # 解析HTML
            tree = etree.HTML(content)
            
            # 使用XPath提取数据
            elements = tree.xpath(xpath)
            
            if not elements:
                logger.warning(f"XPath '{xpath}' 未找到匹配项")
                return []
                
            result = []
            for element in elements:
                item_info = self.extract_item_info(element, res_url)
                if item_info:
                    result.append(item_info)
                    
            logger.info(f"使用XPath '{xpath}' 找到 {len(result)} 个项目")
            return result
            
        except Exception as e:
            logger.error(f"使用XPath提取数据时发生错误: {str(e)}")
            return []

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
                    return title_element[0].xpath("string(.)").strip(), url
                
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
            logger.error(f"提取标题和URL时发生错误: {str(e)}")
            return None, None

    def extract_date_info(self, element):

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


        # re 去掉多余空格
        title = re.sub(r'\s+', ' ', title).strip()

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
                   
            item["date"] = self.extract_date_info(element)
            if not item["date"]:
                item["date"] = None
            
            return item
            
        except Exception as e:
            logger.error(f"提取项目信息时发生错误: {str(e)}")
            return None

    def run_test(self, content, res_url):
        """
        测试XPath提取。
        
        Args:
            content (str): HTML内容
            res_url (str): 响应URL
            
        Returns:
            tuple: (成功标志, XPath表达式)
        """
        try:
            # 获得prompt
            prompt = self.get_prompt(content)
            
            # 查询AI模型,提取XPath表达式
            xpath_response = self.query(input_text=prompt)
            
            if not xpath_response:
                logger.warning("未获取到XPath响应")
                return False, None
                
            # 使用XPath提取数据
            items = self.get_res_by_xpath(xpath_response, content, res_url)
            
            if not items:
                logger.warning(f"使用XPath '{xpath_response}' 未找到项目")
                return False, xpath_response
                
            # 打印提取的信息示例
            for i, item in enumerate(items[:1]):
                logger.info(f"--- 项目 {i+1} ---")
                for key, value in item.items():
                    logger.info(f"{key}: {value}")
                    
            # 验证提取的信息是否完整
            title = items[0].get("title")
            url = items[0].get("url")
            date = items[0].get("date")
            
            if title and url and date:
                logger.info("提取项目信息成功")
                return True, xpath_response
                
            logger.warning("提取项目信息不完整")
            return False, xpath_response
            
        except Exception as e:
            logger.error(f"运行测试时发生错误: {str(e)}")
            return False, None

    def run_mobile(self, url):
        """
        使用移动端用户代理运行测试。
        
        Args:
            url (str): 要测试的URL
            
        Returns:
            tuple: (成功标志, XPath表达式)
        """
            
        try:
            # 获取内容
            content, res_url = self.get_content_with_mobile(url)
            if not content or not res_url:
                logger.warning("移动端获取内容失败")
                return False, None
                
            # 运行测试
            judge, xpath_response = self.run_test(content, res_url)
            return judge, xpath_response
            
        except Exception as e:
            logger.error(f"移动端运行测试时发生错误: {str(e)}")
            return False, None

    def run_window(self, url):
        """
        使用PC端用户代理运行测试。
        
        Args:
            url (str): 要测试的URL
            
        Returns:
            tuple: (成功标志, XPath表达式)
        """
          
        try:
            # 获取内容
            content, res_url = self.get_content_with_window(url)
            if not content or not res_url:
                logger.warning("PC端获取内容失败")
                return False, None
                
            # 运行测试
            judge, xpath_response = self.run_test(content, res_url)
            return judge, xpath_response
            
        except Exception as e:
            logger.error(f"PC端运行测试时发生错误: {str(e)}")
            return False, None

    def run(self, url):
        """
        运行完整的测试流程，先尝试移动端，如果失败则尝试PC端。
        
        Args:
            url (str): 要测试的URL
            
        Returns:
            tuple: (XPath表达式, 终端类型标志)
            终端类型：0表示移动端，1表示PC端，None表示都失败了
        """
        if not url:
            logger.warning("URL为空")
            return None, None
            
        try:
                
            # 先尝试移动端
            logger.info(f"尝试使用移动端访问: {url}")
            judge, xpath_response = self.run_mobile(url)
            
            if judge:
                logger.info(f"移动端提取成功,使用XPath表达式: {xpath_response}")
                return xpath_response, 0
                
            # 如果移动端失败，则尝试PC端
            logger.info(f"移动端失败，尝试使用PC端访问: {url}")
            judge, xpath_response = self.run_window(url)
            
            if judge:
                logger.info(f"PC端提取成功,使用XPath表达式: {xpath_response}")
                return xpath_response, 1
                
            logger.warning("移动端和PC端都提取失败")
            return None, None
            
        except Exception as e:
            logger.error(f"运行测试流程时发生错误: {str(e)}")
            return None, None

    def generate_spider_file(self,template_path, output_title, url, site_name, list_xpath, user_agent):
        """
        根据模板生成新的爬虫文件。

        Args:
            
        """
        try:
            # 读取模板内容
            with open(template_path, 'r', encoding='utf-8') as template_file:
                template_content = template_file.read()

            # 替换模板中的占位符
            spider_content = template_content.replace("{url}", url)
            spider_content = spider_content.replace("{site_name}", site_name)
            spider_content = spider_content.replace("{list_xpath}", list_xpath)
            spider_content = spider_content.replace("{user_agent}", user_agent)
            spider_content = spider_content.replace("{name}", output_title)


            path = os.path.dirname(os.path.abspath(__file__))
            output_path = os.path.join(path,'output',f"{output_title}.py")

            # 写入新的爬虫文件
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(spider_content)

            print(f"成功生成爬虫文件: {output_path}")
        except Exception as e:
            print(f"生成爬虫文件时发生错误: {e}")

    def generate_path(self,url):
        """
        生成爬虫文件的路径。

        Args:
            url (str): 要生成爬虫文件的URL。

        Returns:
            str: 生成的爬虫文件路径。
        """

        path = os.path.dirname(os.path.abspath(__file__))

        template_path = os.path.join(path, "template.py")

        # "https://www.cuhf.edu.cn/180/list.htm"
        domain = urllib.parse.urlparse(url).netloc.replace(".", "_").replace("www_", "")

        output_title = '{domain}_zhaobiao'.format(domain=domain)
        

        return template_path, output_title



if __name__ == "__main__":



    # Example URL
    url = "https://www.cuhf.edu.cn/180/list.htm"
    site_name = 'aaa'

    ai = WoCloudAI()

    template_path, output_title = ai.generate_path(url)

    list_xpath, flag = ai.run(url)

    if list_xpath:

        if flag == 0:
       
            ua = 'Mozilla/5.0 (Linux; Android 14; Xiaomi 13 Build/UP1A.230905.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.170 Mobile Safari/537.36'

            ai.generate_spider_file(template_path, output_title ,url,site_name, list_xpath, ua)


        elif flag == 1:
            
            ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"

            ai.generate_spider_file(template_path, output_title ,url,site_name, list_xpath, ua)
    
        
        
