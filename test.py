import re
import time
import requests
import json
import logging
from lxml import etree


Mobile_UA = "Mozilla/5.0 (Linux; Android 14; Xiaomi 13 Build/UP1A.230905.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.170 Mobile Safari/537.36"

Window_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.170 Safari/537.36"


# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)




def generate_xpath_prompt(contents):
    """生成提取XPath的提示文本"""
    if not contents:
        logger.warning("无内容用于生成提示")
        return ""
        
    prompt = """
        请分析HTML并提取招标公告列表的XPath表达式，遵循以下分析流程：
        步骤1：识别招标列表结构
        - 查找包含重复项的列表结构（如ul/li、table/tr、div组等）
        - 确定招标公告的特征：必须包含标题、日期、链接，且格式统一
        步骤2：构建精确XPath
        - 以//开头，优先使用id、class等特定属性进行定位
        - 为找到的列表项创建XPath，确保选择整个列表项而非子元素
        步骤3：优化表达式
        - 必须使用 `contains(@class, '类名')` 格式来匹配class属性，例如：`//div[contains(@class, 'list')]`
        - 不要使用 `[@class='类名']` 格式，例如：`//div[@class='list']`
        - 使用最简洁但有效的选择器
        示例输出格式：//div[contains(@class, 'list')]//ul//li  
        分析此HTML并仅返回一个最准确的XPath表达式，无需解释：
        {text}
    """
    return prompt.format(text=contents)

def generate_data_xpath_prompt(contents):

    """
    生成用于提取日期的XPath提示文本
    
    Args:
        contents (str): HTML内容
        
    Returns:
        str: 生成的提示文本
    """
    if not contents:
        logger.warning("无内容用于生成日期提取提示")
        return ""
        
    prompt = """
        请分析以下HTML元素并提供一个XPath表达式，用于提取其中的日期信息，遵循以下要求：
        
        1. 识别日期信息的特征：
           - 通常包含数字和分隔符，如2025-04-30、04-30 2025、2025年4月30日等
           - 可能在特定class或id的元素中，如date、time、pubdate等
           - 可能在单独的span、div或其他容器元素中
        
        2. 创建精确的XPath表达式：
           - 使用class、id或其他属性来定位包含日期的元素
           - 对于复合日期（如分散在多个元素中），选择包含完整日期信息的父元素
           - 使用contains()函数匹配class属性
        
        3. 优化表达式：
           - 确保XPath能够准确定位日期元素，不会选择其他内容
           - 如果日期显示在单独标签中，提供定位到文本内容的XPath
           - 如果需要合并多个元素的文本，请提供能获取所有必要部分的XPath
        
        示例输出格式：//div[contains(@class, 'date')]//span
        
        分析此HTML并仅返回一个最准确的用于提取日期的XPath表达式，无需解释：
        {text}
    """
    return prompt.format(text=contents)

def process_p_tag(match):
    p_tag = match.group(0)  # 完整的p标签
    p_content = match.group(1)  # p标签内的内容
            
            # 移除HTML实体和多余空格后再计算实际长度
    clean_content = re.sub(r'&nbsp;|&lt;|&gt;|&amp;|&quot;|&apos;', ' ', p_content)
    clean_content = re.sub(r'\s+', ' ', clean_content).strip()
            
    if len(clean_content) > 50:
        logger.debug(f"删除长度为 {len(clean_content)} 的p标签内容")
        return ''  # 返回空字符串，移除整个p标签
    return p_tag  # 保留短内容p标签

def clean_blank_html(html_content):
        
        
        # 处理空格和换行
        html_content = re.sub(r'\s+', ' ', html_content)
         # 去除空标签
        for _ in range(10):  # 通常3次迭代足以处理大多数嵌套情况
            # 处理完全为空的标签，如 <div class="searchbtn"></div>
            html_content = re.sub(r'<([a-zA-Z]+)([^>]*)></\1>', '', html_content)
            
            # 处理包含空格的空标签
            html_content = re.sub(r'<([a-zA-Z]+)([^>]*)>\s*</\1>', '', html_content)
            
            # 处理包含HTML空格实体的空标签
            html_content = re.sub(r'<([a-zA-Z]+)([^>]*)>(&nbsp;)*</\1>', '', html_content)


        return html_content

def remove_html_tags(html_content):

        tags_to_remove = ['head', 'script', 'style', 'meta', 'link', 'title', 'img', 'input']
        for tag in tags_to_remove:
            # 处理带有关闭标签的情况 - 不区分大小写
            html_content = re.sub(rf'<{tag}[\s\S]*?>.*?</{tag}>', '', html_content, flags=re.IGNORECASE)
            
            # 处理自闭合标签的情况 - 不区分大小写
            html_content = re.sub(rf'<{tag}[^>]*?/>', '', html_content, flags=re.IGNORECASE)
            
            # 处理没有显式关闭的标签 - 不区分大小写
            html_content = re.sub(rf'<{tag}[^>]*?>', '', html_content, flags=re.IGNORECASE)

        return html_content

def remove_foot_tags(html_content):

        # 递归地删除整个 footer、header、nav 区域及其所有内容
        # 使用非贪婪匹配并确保匹配完整的开始和结束标签对
        patterns_to_remove = [
            # 匹配class或id包含footer的div
            r'<div[^>]*?(?:class|id)=[\"\']?[^\"\']*?footer[^\"\']*?[\"\']?[^>]*?>[\s\S]*?</div>',
            # 匹配class或id包含header的div
            r'<div[^>]*?(?:class|id)=[\"\']?[^\"\']*?header[^\"\']*?[\"\']?[^>]*?>[\s\S]*?</div>',
            # 匹配class或id包含nav的div
            r'<div[^>]*?(?:class|id)=[\"\']?[^\"\']*?nav[^\"\']*?[\"\']?[^>]*?>[\s\S]*?</div>',
            # 匹配专用footer标签
            r'<footer[\s\S]*?</footer>',
            # 匹配专用header标签
            r'<header[\s\S]*?</header>',
            # 匹配专用nav标签
            r'<nav[\s\S]*?</nav>'
        ]
        
        # 深度嵌套处理 - 循环多次以处理嵌套情况
        for _ in range(5):  # 通常3次迭代足以处理大多数嵌套深度
            for pattern in patterns_to_remove:
                # 使用非贪婪匹配并匹配div标签内的所有内容
                html_content = re.sub(pattern, '', html_content, flags=re.IGNORECASE)


        return html_content

def clean_html(html_content):
    """
    清理HTML内容，去除无用标签和内容
    
    Args:
        html_content (str): 原始HTML内容
        
    Returns:
        str: 清理后的HTML内容
    """
    if not html_content:
        return ""
        
    try:

        # 选择body部分,BODY标签
        body_content = re.search(r'<body.*?>([\s\S]*?)</body>', html_content, re.IGNORECASE)
        if body_content:
            html_content = body_content.group(1)
        else:
            logger.warning("未找到有效的body内容，使用原始HTML")

        # 去除注释
        html_content = re.sub(r'<!--[\s\S]*?-->', '', html_content)

         # 去除空标签
        html_content = clean_blank_html(html_content)

         # 去除不必要的标签
        html_content = remove_html_tags(html_content)
  
        # 去除脚注
        html_content = remove_foot_tags(html_content)

        # 处理p标签里面内容长度>50得删除，小于50的保留
        html_content = re.sub(r'<p[^>]*>([\s\S]*?)</p>', process_p_tag, html_content, flags=re.IGNORECASE)

        # 去除空标签
        html_content = clean_blank_html(html_content)


        return html_content
    
    except Exception as e:
        logger.error(f"清理HTML内容时发生错误: {str(e)}")
        return html_content    

def fetch_content(url, timeout=30, max_retries=3, retry_delay=2, ua=None):
    """获取URL的内容"""
    headers = {"User-Agent": ua if ua else "Mozilla/5.0 (Linux; Android 14; Xiaomi 13 Build/UP1A.230905.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.170 Mobile Safari/537.36"}

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()  # 检查请求是否成功
            response.encoding = response.apparent_encoding  # 动态设置编码
            return response.text
        except requests.RequestException as e:
            logger.warning(f"尝试 {attempt + 1}/{max_retries} 获取URL内容失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logger.error(f"获取URL内容完全失败: {e}")
                return None
        except Exception as e:
            logger.error(f"发生未知错误: {e}")
            return None

def make_api_request(url, headers, data):
    """发送API请求"""
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"API 请求失败: {e}")
        return None
    except Exception as e:
        logger.error(f"发生未知错误: {e}")
        return None

def siliconflow_api(prompt):
        
        """调用SiliconFlow API"""
        api_url = "https://api.siliconflow.cn/v1/chat/completions"
        api_headers = {
            "Authorization": "Bearer sk-sdrouklhpvfgrzxlsyjwegoebspzmlnrilqjohqohzidtnjs",  # 替换为您的Token
            "Content-Type": "application/json"
        }

        model_list = ["Qwen/Qwen3-8B", "THUDM/GLM-Z1-9B-0414",'Qwen/Qwen2.5-7B-Instruct','Qwen/Qwen3-30B-A3B','Qwen/Qwen2-1.5B-Instruct']

        api_data = {
            "model": "Qwen/Qwen3-8B",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False, "max_tokens": 4096, "enable_thinking": False, "thinking_budget": 4096,
            "min_p": 0.05, "stop": None, "temperature": 0.5, "top_p": 0.7, "top_k": 50,
            "frequency_penalty": 0.5, "n": 1, "response_format": {"type": "text"}, "tools": []
        }

        api_response = make_api_request(api_url, api_headers, api_data)

        if api_response:
            xpath = json.loads(api_response).get("choices")[0].get("message").get("content")
            logger.info(f"生成的XPath: {xpath}")
            return xpath
        else:
            logger.error("API 请求失败")
            return None

def extract_tender_title_url_info(a_tag_list):

      # 找到文本最长的 <a> 标签
        longest_a = max(a_tag_list, key=lambda a: len((a.text or "").strip()))
        title = (longest_a.get('title') or longest_a.text.strip())
        url = longest_a.get('href').strip()

        if title and url:
            # 如果标题和链接都存在，返回它们
            return title, url

        # 如果没有找到有效的标题和链接，返回空字符串
        return None, None

def extract_singal_a_info(element):
        '''
        提取a标签的标题和URL信息。
        '''
        url = element.get("href",None)

        title = element.get("title") or element.xpath('string(.)').strip()
      
        return title, url

def extract_data(element):

    # 2. 常规日期格式 YYYY-MM-DD 或类似格式
    date_pattern = re.compile(r'(\d{4})[-/.年\\](\d{1,2})[-/.月\\](\d{1,2})')
    
    # 先从整个元素内容中查找
    text = element.xpath('string(.)').strip()
    date_match = date_pattern.search(text)
    
    # 格式化常规日期
    if date_match:
        groups = date_match.groups()
        year, month, day = groups[:3]
        date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        return date
    
    
    # 3. 尝试其他可能的日期格式，比如反向格式 MM-DD-YYYY
    alt_date_pattern = re.compile(r'(\d{1,2})[-/.月](\d{1,2})[-/.日]?[,\s]*(\d{4})')
    alt_date_match = alt_date_pattern.search(text)
    if alt_date_match:
        month, day, year = alt_date_match.groups()
        date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        return date
    
    # 4. 尝试其他可能的日期格式，比如反向格式 DD-YYYY-MM
    alt_date_pattern = re.compile(r'(\d{1,2})?[,\s]*(\d{4})[-/.年](\d{1,2})')
    alt_date_match = alt_date_pattern.search(text)
    if alt_date_match:
        day, year, month = alt_date_match.groups()
        date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        return date
    
    return None

def extract_tender_data_info(element):
    """
    提取招标公告的日期信息
    
    Args:
        element: lxml元素对象
        data_xpath: 可选的日期提取XPath
        
    Returns:
        str: 提取到的日期字符串，格式化为YYYY-MM-DD
    """
    # 首先使用通用提取日期，格式为yyyy-mm-dd 间隔符任意
    data = extract_data(element)
    if data:
        return data
    
def extract_tender_info(element):
    """
    通用提取函数，根据元素类型选择合适的提取策略
    
    Args:
        element: lxml元素对象
        
    Returns:
        dict: 包含title, url, date的字典
    """
        
    title = None
    url = None
    # 提取标题和 URL


     # 如果是a元素，直接提取
    if element.tag.lower() == "a":
       
        title,url = extract_singal_a_info(element)
        title = title
        url = url

    else:
        a_tag_list = element.xpath('.//a[@href]')
        if a_tag_list:
            title, url = extract_tender_title_url_info(a_tag_list)
            title = title
            url = url
       

    return title,url

def validate_xpath(html_content, list_xpath):
    """验证XPath表达式是否正确"""
    try:
        tree = etree.HTML(html_content)
        elements = tree.xpath(list_xpath)

        if elements:

            logger.info(f"list_xpath '{list_xpath}' 验证成功，找到 {len(elements)} 个元素")
            
            tender_info_list = []
            for element in elements:
               
                title,url = extract_tender_info(element)
                date = extract_tender_data_info(element)

                if title and url and date:
                    # 如果标题、链接和日期都存在，添加到列表中
                    tender_info = {
                        "title": title,
                        "url": url,
                        "date": date
                    }
                    tender_info_list.append(tender_info)
                    logger.info(f"提取招标信息成功: {tender_info}")
                else:
                    logger.warning("提取招标信息失败，标题或链接为空")

            return True
        else:
            logger.warning(f"XPath '{xpath}' 验证失败，未找到任何元素")
            return False
    except Exception as e:
        logger.error(f"XPath 验证发生错误: {e}")
        return False



# https://www.fcgzy.edu.cn/news/tzgg/
# https://www.hebuee.edu.cn/tzgg1.htm
# http://sdycu.edu.cn/index/tzgg.htm
# https://www.zznu.edu.cn/Bidding/index.html
# https://www.nbpt.edu.cn/744/list.htm

# 主要代码
if __name__ == "__main__":
    
    target_url = "http://dlu.edu.cn/xwfb/xxgg.htm"  # 替换为目标URL
    
    html_content = fetch_content(target_url,ua = Window_UA)

    clean_content = clean_html(html_content)

    prompt = generate_xpath_prompt(clean_content)

    # with open("prompt.txt", "w", encoding="utf-8") as f:
    #     f.write(prompt)
    #     logger.info("提示文本已保存到 prompt.txt")

    xpath = siliconflow_api(prompt)
      
    if validate_xpath(html_content, xpath):

        logger.info("XPath 验证成功，可以使用")
        
 










