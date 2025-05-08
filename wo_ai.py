import json
import re
import requests
import random
import os
import urllib


X_YP_Access_Token = "a36a90f6-d119-4b50-970f-30894a2f39fa"


class WoCloudAI:

    def __init__(self):
        self.url = "https://panservice.mail.wo.cn/wohome/ai/assistant/query"
        self.x_yp_client_id = [
            "1001000035",
            "1001000036",
            "1001000037",
            "1001000021",
            "1001000022",
            "1001000023",
            "1001000024",
            "1001000025",
            "1001000026",
            "1001000027",
            "1001000028",
            "1001000029",
            "1001000030",
            "1001000031",
            "1001000032",
            "1001000033",
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
        self.headers = {
            "Host": "panservice.mail.wo.cn",
            "Connection": "close",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Android WebView";v="127", "Chromium";v="127"',
            "X-YP-Access-Token": X_YP_Access_Token,
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

    def query(self, input_text="aaa",  model_id=0, tag=0, history=None):

        # model_id: 0 是默认模型，1 是 deepseek
        # input_text： 输入文本

        if history is None:
            history = []

        data = {"input": input_text, "modelId": model_id, "tag": tag, "history": history}

        try:
            response = requests.post(self.url, headers=self.headers, json=data)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            full_response = ""  # Initialize an empty string to store the full response
            for line in response.iter_lines():
                decoded_line = line.decode("utf-8").replace("data:", "").strip()
                if len(decoded_line) != 0:
                    json_line = json.loads(decoded_line)  # Parse each line as JSON 
                    full_response += json_line["response"]  # Append the 'response' value
                    
            # print("Full response:", full_response) 
            return full_response  # Return the full response

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    #  - 最多使用3个div层级，可以使用//跳过中间层级或使用特定的属性直接定位
    def get_prompt(self, contents):

        prompt = """
        提取招标公告列表的XPath表达式，仅返回一个准确的XPath表达式，无需其他内容。

        目标元素特征：
        - 通常在列表结构中(如ul,tr,div等)
        - 返回的必须是完整的列表项元素本身，而非其中的链接元素
        - 必须以//开头，使用特定的属性直接定位
       
        
        分析此HTML并返回最简洁有效的XPath，确保表达式停止在列表项级别而不深入到子元素:
        {text}
        """
        return prompt.format(text=contents)
        
    def get_content(self,url):

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            "User-Agent": "Mozilla/5.0 (Linux; Android 8; Vivo X21 Build/O11019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.91 Mobile Safari/537.36",
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None
        
         # 尝试从Content-Type头部获取正确的编码
        content_type = response.headers.get('Content-Type', '')
        encoding_match = re.search(r'charset=(\S+)', content_type)
        
        if encoding_match:
            encoding = encoding_match.group(1)
        else:
            # 如果响应头没有指定编码，使用apparent_encoding
            encoding = response.apparent_encoding
        
        # 显式设置响应的编码
        response.encoding = encoding
        
        # 处理响应内容
        # 例如，解析HTML、提取数据等

        cleaned_response = self.clean_response(response.text)

        return cleaned_response,response.url

    def clean_response(self, full_response):
       
        # 使用正则表达式或其他方法清理响应
        # 例如，去除多余的空格、换行符等
        # 选取body部分
        body_match = re.search(r"<body.*?>(.*?)</body>", full_response, re.DOTALL)
        if body_match:
            full_response = body_match.group(1)
        
        # 剔除css，script等标签
        full_response = re.sub(r"<script.*?>.*?</script>", "", full_response, flags=re.DOTALL)
        full_response = re.sub(r"<style.*?>.*?</style>", "", full_response, flags=re.DOTALL)


        return full_response

    def get_res_by_xpath(self, xpath, content, res_url):
        # 使用lxml或BeautifulSoup等库解析HTML并提取数据
        from lxml import etree

        # 解析HTML
        tree = etree.HTML(content)

        # 使用XPath提取数据
        elements = tree.xpath(xpath)

        result = []
        for element in elements:
            # 提取每个列表项的有用信息，而不是直接转换整个HTML
            item_info = self.extract_item_info(element,res_url)
            result.append(item_info)
            
        return result

    def extract_title_url_info(self, title_element):

        if title_element is None:
            return None
        
        if len(title_element) == 1:

            title_attr = title_element[0].get("title")
            if title_attr and title_attr.strip():
                return title_attr.strip(),title_element[0].get("href")
            else:
                # 如果没有title属性或title为空，则使用元素文本内容
                return title_element[0].xpath("string(.)").strip(),title_element[0].get("href")
            
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
            
            return longest_text, longest_url  # 返回最长文本和对应的URL

    def extract_item_info(self, element,res_url):
        """从列表项元素中提取标题、日期和链接等信息"""

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

    def run(self, url):

        # 获取网页内容
        content,res_url = self.get_content(url)

        # 获得prompt
        prompt = self.get_prompt(content)

        # 查询AI模型,提取XPath表达式
        xpath_response = self.query(input_text=prompt)

        print("XPath response:", xpath_response)

        if xpath_response is None:
            print("Failed to get XPath response.")
            return

        # 使用XPath提取数据
        items = self.get_res_by_xpath(xpath_response, content, res_url)

        # 打印提取的信息，而不是原始HTML
        for i, item in enumerate(items[:3]):  # 只打印前3项作为示例
            print(f"\n--- 项目 {i+1} ---")
            for key, value in item.items():
                    print(f"{key}: {value}")


# https://cs.nuaa.edu.cn/10847/list.htm
# https://www.njitt.edu.cn/tzgg/list.htm
# https://zbcag.jsit.edu.cn/cggghwl/index.chtml
# https://lntdxy.com/sylm/zbgg.htm


# https://www.whit.edu.cn/index/zcyzc.htm
# https://www.gzgsc.edu.cn/zsyzb/cgzb/cgzb.htm


if __name__ == "__main__":

    ai = WoCloudAI()

    # Example URL
    url = "http://www.haue.edu.cn/xwdt/tzgg.htm"

    ai.run(url)




