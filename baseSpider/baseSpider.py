import inspect
import json
import random
from urllib.parse import urljoin
from scrapy.exceptions import CloseSpider
import scrapy
from baseSpider.utils.BloomFilter import bloomFilter
from baseSpider.utils.RedisManage import RedisConnectionManager
from datetime import datetime
from baseSpider.items import BaseItem,RequestItem
from scrapy import signals
import logging
import re
from scrapy.selector.unified import Selector



logger = logging.getLogger(__name__)


class SpiderMeta(type):
    def __new__(mcs, name, bases, attrs):
        # 先合并所有父类的 custom_settings
        base_settings = {}
        for base in reversed(bases):
            base_custom = getattr(base, 'custom_settings', None)
            if isinstance(base_custom, dict):
                base_settings |= base_custom

        custom_settings = attrs.get('custom_settings', {})
        if not isinstance(custom_settings, dict):
            custom_settings = {}

        # 需要叠加的 key
        merge_keys = ['DOWNLOADER_MIDDLEWARES', 'ITEM_PIPELINES', 'SPIDER_MIDDLEWARES', 'EXTENSIONS']
        merged = base_settings.copy()
        for key, value in custom_settings.items():
            if key in merge_keys and key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                # 叠加（父类+子类，子类优先）
                merged[key] = merged[key].copy()
                merged[key].update(value)
            else:
                merged[key] = value

        attrs['custom_settings'] = merged
        return super().__new__(mcs, name, bases, attrs)




class BaseSpiderObject(scrapy.Spider,metaclass=SpiderMeta):

    name = "base"
    start_urls = ''

    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = None  # 用于拼接详情页网址
    province = None  # 必填，爬虫省份
    city = None  # 必填，爬虫城市
    county = None  # 选填，爬虫区/县
    site_name = None
    source = None # 数据来源，爬虫名称
    page_over = False # 翻页
    current_directory = None
    
    timeRange = 7 # 爬虫时间范围，单位为天,0为当天，1为前一天，2为前两天，3为前三天，4为前四天，5为前五天，6为前六天，7为前七天
    crawl_today = datetime.now() # 爬虫开始时间
    last_publish_time = None # 最新发布时间

    insertCount = 0 # 总任务数量
    successCount = 0 # 成功数量

    failed_urls = [] # 失败的url

    max_page = 2 # 最大页数
    init_failed_count = 0 # 初始化失败数量
    max_failures = 10 # 最大失败数量

    # stop_flag = False      # 终止标识
    task_redis_server = RedisConnectionManager.get_connection() # Redis连接

    detail_xpath ='//body' # 详情页xpath


    custom_settings = {
         'DOWNLOADER_MIDDLEWARES': {
                "baseSpider.middlewares.BaseDownloaderMiddleware": 3, 
                "baseSpider.middlewares.BaseHeaderMiddleware": 1,  # 添加请求头
                "baseSpider.middlewares.PlaywrightMiddleware": 2,  # 使用playwright渲染页面
                "baseSpider.middlewares.BaseRetryMiddleware": 600,  # 重试
                'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,  # 重试中间件禁用
            },
            'ITEM_PIPELINES': {
                "baseSpider.pipelines.baseSpiderPipeline": 300,
            },
            'ROBOTSTXT_OBEY': False,
            'DOWNLOAD_DELAY': 3,
            'CONCURRENT_REQUESTS_PER_IP': 8,
            'RETRY_ENABLED': True,
            'TWISTED_REACTOR' : "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            'LOG_LEVEL':'INFO',
    }

    def __init__(self):

        directory = inspect.getmodule(self.__class__).__file__
        self.current_directory = directory.split('/spiders')[0].split('/')[-1]
        self.source = self.start_urls.split('/')[2]

        self.task_redis_server.rpush('running_spiders', self.name)
        logger.info(f'Spider {self.name} started and added to running queue.')
 
    def get_base_item(self)->BaseItem:
        
        """
        返回一个包含基本信息的 BaseItem 对象。
        
        Args:
            无。
        
        Returns:
            BaseItem: 包含以下基本信息的 BaseItem 对象：
                - source: 数据来源
                - site_name: 站点名称
                - province: 省份
                - city: 城市
                - county: 区县
        
        """
        """
        返回 BaseItem 对象。
        
        Args:
            baseItem (BaseItem): 待返回的 BaseItem 对象。
        
        Returns:
            BaseItem: 返回的 BaseItem 对象。
        
        """

        baseItem = BaseItem()
        baseItem['source'] = self.source
        baseItem['site_name'] = self.site_name
        baseItem['province'] = self.province
        baseItem['city'] = self.city
        baseItem['county'] = self.county

        return baseItem

    # 判断时间超过timeRange天的url不再爬取
    def is_time_out(self, time:datetime)->bool:
        
        """
        判断给定的时间是否超出了设定的时间范围。
        
        Args:
            time (datetime.datetime): 待判断的时间点。
        
        Returns:
            bool: 若给定的时间点超出了设定的时间范围，则返回True；否则返回False。
        
        """
        if abs((time.date() - self.crawl_today.date()).days) > self.timeRange:
            
            return True

        return False
    
    # 提取数字
    def extract_number(self, string:str)->str:
        """
        从字符串中提取2024-11-12。
        
        Args:
            string (str): 待提取的字符串。
        
        Returns:
            str: 提取出的数字字符串。
        
        """
        try:
            number = re.search(r'\d{4}-\d{2}-\d{2}', string).group()
        except:
            number = None

        return number

    def format_time(self, publish_time)->datetime:
        """
        格式化时间字符串，将发布时间转换为 datetime 对象。
        
        Args:
            publish_time (str): 发布时间字符串，格式为年月日时分秒或年月日等。
        
        Returns:
            datetime: 格式化后的 datetime 对象，格式为 '%Y-%m-%d'。
        
        """
    
        try:
            time = datetime.strptime(str(publish_time), '%Y-%m-%d')

        except:

            logger.error("Time format error")

        return time
    
    def format_time_to_str(self, publish_time)->str:
        """
        格式化时间字符串，将发布时间转换为 datetime 对象。
        
        Args:
            publish_time (str): 发布时间字符串，格式为年月日时分秒或年月日等。
        
        Returns:
            datetime: 格式化后的 str 对象，格式为 '%Y-%m-%d'。
        
        """
        if '(' in publish_time:
            publish_time = publish_time.replace('(', '-')
        if ')' in publish_time:
            publish_time = publish_time.replace(')', '-')
        if '/' in publish_time:
            publish_time = publish_time.replace('/', '-')
        if ' ' in publish_time:
            publish_time = publish_time.replace(' ', '')
        if '.' in publish_time:
            publish_time = publish_time.replace('.', '-')
        if '[' in publish_time:
            publish_time = publish_time.replace('[', '')
        if ']' in publish_time:
            publish_time = publish_time.replace(']', '')
        if '年' in publish_time:
            publish_time = publish_time.replace('年', '-')    
        if '月' in publish_time:
            publish_time = publish_time.replace('月', '-')
        if '日' in publish_time:
            publish_time = publish_time.replace('日', '')


        publish_time = self.extract_number(publish_time)

        if len(publish_time) > 10:
            publish_time = publish_time[:10]

        try:
            return publish_time

        except:

            logger.error("Time format error")
   
    def is_url_having(self, url:str)->bool:
        """
        判断给定的URL是否在布隆过滤器中。
        
        Args:
            url (str): 待判断的URL。
        
        Returns:
            bool: 若URL在布隆过滤器中，返回True；否则返回False
        """
        
        if bloomFilter.is_contained(url):
            return True
        
        return False
    
    def add_url(self,url:str):
        """
        将给定的URL添加到布隆过滤器中。
        
        Args:
            url (str): 待添加的URL。
        
        Returns:
            None
        """
        bloomFilter.add(url)
        
    def is_time_stop(self,publishTime:str)->bool:
        """
        判断当前时间是否超过了发布时间所指定的时间限制
        
        Args:
            publishTime (str): 发布时间，格式为"%Y-%m-%d"
        
        Returns:
            bool: 如果当前时间超过了发布时间所指定的时间限制，返回True；否则返回False
        """
  
        time = self.format_time(publishTime)
        
        return self.is_time_out(time)
    
    def has_next_page(self,baseItem:BaseItem,page:int)->bool:
        """
        判断是否有下一页
        
        Args:
            baseItem (BaseItem): 包含基础信息的对象
            page (int): 当前页码
        
        Returns:
            bool: 如果存在下一页，则返回True；否则返回False
        
        """

        # 判断是否有下一页
        if not self.is_time_stop(baseItem['publish_time']) and page < self.max_page:
            
            return True
        
        return False
        
    def request_next_page(self, baseItem, page, request_params):
        """
        封装翻页请求逻辑，根据当前页码和内容决定是否继续翻页并发起下一页请求。
        
        Args:
            baseItem (BaseItem): 当前页面的内容项
            page (int): 当前页码
            param (str): 当前 URL 模板

        Returns:
            None
        """
        # 判断是否有下一页
        if self.has_next_page(baseItem, page):
            
            # 爬取下一页
            logger.debug(f"Requesting next page: {page}")
            return self.parse_task(RequestItem(**request_params))
        else:
            self.page_over = True
            logger.debug(f"No next page or stopping condition met at page {page}.")

    def update_publish_time(self, publish_time:str):
        """
        更新发布时间，将发布时间转换为datetime类型，然后将其赋值给self.publish_time属性。
        
        Args:
            publish_time (str): 发布时间字符串，格式为"%Y-%m-%d %H:%M:%S"
        
        Returns:
            None
        """

        new_publish_time = self.format_time(publish_time)

        if self.last_publish_time is None or new_publish_time > self.last_publish_time:
            self.last_publish_time = new_publish_time
            
    def calculate_task_item(self,task:BaseItem):
        
        """

        Args:
            task (BaseItem): 待插入的任务对象，需为BaseItem或其子类的实例。

        Returns:
            None

        """

        # 检查task['url'],task['publish_time'] 是否为空
        if task['url'] is None:
            # 将url插入到url_error队列
            self.insert_url_error()
            raise CloseSpider('url xpath is changed')
        if task['publish_time'] is None:
            # 将time插入到time_error队列
            self.insert_time_error()
            raise CloseSpider('time xpath is changed')

        # 更新发布时间
        self.update_publish_time(task['publish_time'])

        # 检查任务是否满足停止条件,如果时间超过timeRange天则跳过
        if self.is_time_stop(task['publish_time']):
            
            logger.debug("Stopping spider due to time condition.")
            # raise CloseSpider(reason='Time Stop Condition Met')
            return False
 
        # 检查任务是否满足停止条件,如果url已经爬取过则跳过
        if self.is_url_having(task['url']):
            logger.debug("Url exit.")
            return False

        # 计算任务数量
        try:    
                self.insertCount += 1
                self.failed_urls.append(task['url'])

        except Exception as e:
                
                logger.error("Insert task item error",e)

        return True

    def update_state(self):

        if self.insertCount == self.successCount and self.page_over:

            return True

    def insert_url_error(self):
        
        try:
            data = {
                'source': self.source,
                'name': self.name,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            self.task_redis_server.lpush('url_error',json.dumps(data))
        
        except:
            logger.error("Insert url queue error")

    def insert_time_error(self):
        
        try:
            data = {
                'source': self.source,
                 'name': self.name,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            self.task_redis_server.lpush('time_error',json.dumps(data))
        except:
            logger.error("Insert time queue error")

    def get_key(self):
        return  "task_log:" + self.crawl_today.strftime('%Y-%m-%d') + ":"  + self.source + ":" + self.name

    def init_source_log(self,key):
       
        # 参数1 今天网站更新的总数量
        # 参数2 今天网站爬取的成功数量
        # 参数3 今天网站爬取的失败数量
        # 参数4 本次爬取成功的数量 
        # 参数5 本次爬取失败的数量
        # 参数6 本网站最新的发布时间
        # 参数7 最近一次爬取的时间
        # 参数8 本轮爬虫运行的时间
        # 参数9 今天爬取的次数
        # 参数10 失败的url,存储的是url的列表
        # key 为 source + 日期

        # 判断key是否存在
        if not self.task_redis_server.exists(key):

            data = {
                'name': self.name,
                'source': self.source,
                'site_name': self.site_name,
                'last_publish_time': '',
                'today_all_request': 0,
                'today_success_request': 0,
                'today_fail_request': 0,
                'this_time_all_request': 0,
                'this_time_success_request': 0,
                'this_time_fail_request': 0,
                'last_time': '',
                'run_time': '',
                'crawl_count': 0,
                'failed_urls': json.dumps([])
            }

            # 存储数据 
            self.task_redis_server.hmset(key, data)

    def read_source_log(self,key):

        data = self.task_redis_server.hgetall(key)

        # 转为字典
        return {
            'name': data['name'],
            'source': data['source'],
            'site_name': data['site_name'],
            'state': 'failure',
            'last_publish_time': data['last_publish_time'],
            'today_all_request': int(data['today_all_request']),
            'today_success_request': int(data['today_success_request']),
            'today_fail_request': int(data['today_fail_request']),
            'this_time_all_request': int(data['this_time_all_request']),
            'this_time_success_request': int(data['this_time_success_request']),
            'this_time_fail_request': int(data['this_time_fail_request']),
            'last_time': data['last_time'],
            'run_time': data['run_time'],
            'crawl_count': int(data['crawl_count']),
            'failed_urls':  json.loads(data['failed_urls'])
        }
  
    def write_source_log(self,key,data:dict):
        
        data['failed_urls'] = json.dumps(data['failed_urls'])

        # 存储数据
        self.task_redis_server.hmset(key, data)

        # 对数据进行排序,更新key的分数,分数为时间戳
        score = datetime.now().timestamp()

        if self.check_member_exists(key):
            self.task_redis_server.zadd('key_sorted_set', {key: score},xx=True)
        else:
            self.task_redis_server.zadd('key_sorted_set', {key: score})

    def check_member_exists(self, key):
        # 检查成员是否存在于有序集合中
        score = self.task_redis_server.zscore('key_sorted_set', key)
        if score is not None:
            return True
        else:
            return False

    def insert_task_log(self):
        """
        插入任务日志
        
        Args:
            无参数
        
        Returns:
            无返回值
        
        Raises:
            无异常抛出
        
        """
        
       
        key = self.get_key()

        # 初始化日志
        self.init_source_log(key)

        # 读取日志
        data = self.read_source_log(key)

        # 计算状态
        if self.update_state():
            data['state'] = 'success'
         
        # 添加当前目录
        data['current_directory'] = self.current_directory

        #  计算本次爬总数量
        data['this_time_all_request'] = self.insertCount

        # 计算本次爬取成功数量
        data['this_time_success_request'] = self.successCount

        # 计算本次爬取失败数量
        data['this_time_fail_request'] = self.insertCount - self.successCount

        # 计算今日总请求数量
        data['today_all_request'] = data['today_all_request'] +  self.insertCount -  data['today_fail_request']

        # 计算今日成功数量
        data['today_success_request'] += self.successCount

        # 计算今日失败数量
        data['today_fail_request'] = data['today_all_request'] - data['today_success_request']

        # 计算最近一次爬取时间
        data['last_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 计算爬虫运行时间,转化为秒
        data['run_time'] = str((datetime.now() - self.crawl_today).seconds)

        # last_publish_time
        if self.compare_time(data['last_publish_time']):
            data['last_publish_time'] = self.last_publish_time.strftime('%Y-%m-%d')

        # 计算爬取次数
        data['crawl_count'] += 1

        # 计算失败的url
        data['failed_urls'] = self.failed_urls
       
        # 写入日志
        self.write_source_log(key,data)

        # 输出日志
        self.log_info(data)

        # 清空任务数量
        self.task_redis_server.lrem('running_spiders', 0, self.name)

    def compare_time(self, time:str):


        if self.last_publish_time is None:
            return False

        if time == '' or time is None:
            return True
        
        datetime_object = datetime.strptime(time, '%Y-%m-%d')
        # 比较时间,如果当前时间大于上次发布时间,则返回True
        if self.last_publish_time > datetime_object:
            
            return True
        else:
            return False

    def log_info(self,data):
         # 输出日志
        logger.error(
            f"\nname: {data['name']}, \n"
            f"source: {data['source']}, \n"
            f"site_name: {data['site_name']}, \n"
            f"state: {data['state']}, \n"
            f"current_directory: {data['current_directory']},\n"
            f"last_publish_time: {data['last_publish_time']}, \n"
            f"this_time_all_request: { data['this_time_all_request']}, \n" 
            f"this_time_success_request: {data['this_time_success_request']},\n"
            f"this_time_fail_request: {data['this_time_fail_request']},\n"
            f"today_all_request: {data['today_all_request']},\n"
            f"today_success_request: {data['today_success_request']},\n"
            f"today_fail_request: {data['today_fail_request']},\n"
            f"last_time: {data['last_time']},\n"
            f"run_time(second): {data['run_time']},\n"
            f"crawl_count: {data['crawl_count']}\n"
        )
        
    # 爬虫关闭时调用
    def closed(self, reason):
            # 插入任务日志
            self.insert_task_log()

    def parse_task(self,tasks:RequestItem):

        time.sleep(random.randint(1, 3))

        if tasks['method'].upper() == 'GET':

            if tasks['params'] is None:
                return scrapy.Request(tasks['url'],method='get',callback=tasks['callback'],errback=tasks['errback'],dont_filter=True,meta=tasks['meta'],cookies=tasks['cookies'],headers=tasks['headers'])
            else:
                return scrapy.Request(tasks['url'],method='get',callback=tasks['callback'],errback=tasks['errback'],dont_filter=True,meta=tasks['meta'],cookies=tasks['cookies'],headers=tasks['headers'],body=json.dumps(tasks['params']))

        if tasks['method'].upper() == 'POST':

            if tasks['request_body'].lower() == 'formdata':
                return scrapy.FormRequest(tasks['url'],method='post',callback=tasks['callback'],errback=tasks['errback'],dont_filter=True,meta=tasks['meta'],cookies=tasks['cookies'],headers=tasks['headers'],formdata=tasks['params'])

            elif tasks['request_body'].lower() == 'json':
                return scrapy.Request(tasks['url'],method='post',callback=tasks['callback'],errback=tasks['errback'],dont_filter=True,meta=tasks['meta'],cookies=tasks['cookies'],headers=tasks['headers'],body=json.dumps(tasks['params']))

    def parse(self,response):
        pass

    def parse_content_detal(self,response):
        
        # 获取详情页数据
        item:BaseItem = self.parse_content(response)  
        
        yield item
    
    def errback_httpbin(self,failure):
        
        # 如记录此网页url是失败的，失败的url数量加1
        self.init_failed_count += 1
        logger.error(f"Request failed: {failure.value} (Total failures: {self.init_failed_count})")

        # 如果失败的url数量超过最大失败数量则停止爬虫
        if self.init_failed_count > self.max_failures:
            logger.error(f"Maximum number of failures ({self.max_failures}) reached. Stopping the spider immediately.")
            
            raise CloseSpider('max_failures')
        
            # 设置终止标识,并在pipeline中关闭爬虫
            # self.stop_flag = True

            # 执行关闭爬虫
            # self.closed('max_failures')
            # 立即终止进程
            # os._exit(1)

    def parse_content(self,response)->BaseItem:
        """
        解析响应内容，根据响应类型（HTML或JSON）填充Item对象。
        
        Args:
            response (Response): 响应对象，包含待解析的响应内容。
        
        Returns:
            BaseItem: 填充后的Item对象。
        
        """
         
        item = response.meta['item']
        
        # response 返回的类型包括html和json两种格式

         # 尝试从 Content-Type 头中获取响应类型
        content_type = response.headers.get('Content-Type', b'').decode('utf-8')

        if 'json' in content_type:
            # 解析JSON
            item = self.parse_json(response, item)
        elif 'html' in content_type:
            # 解析HTML
            item = self.parse_html(response, item)
        else:
            # 如果无法从 Content-Type 确定类型，尝试其他方法
            item = self.determine_response_type(response, item)

        return item

    def determine_response_type(self, response, item: BaseItem) -> BaseItem:
        # 尝试通过响应内容来确定类型
        try:
            # 尝试解析为JSON
            if json.loads(response.text):
                return self.parse_json(response, item)
            
        except json.JSONDecodeError:
            # 如果解析失败，假设为HTML
            return self.parse_html(response, item)

    def parse_html(self,response,item:BaseItem)->BaseItem:
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
            item = self.parse_contents_with_xpath(response, item, self.detail_xpath)

            # 提取附件内容
            item = self.request_attachment_contents(response, item)


            return item


        except Exception as e:

            logger.error("Parse content error",e)
            return None
        
    def parse_contents_with_xpath(self,response,item:BaseItem,xpath:str)->BaseItem:
        '''
        使用传入的 xpath 提取内容和附件链接。

        Args:
            response: Scrapy 的 Response 对象。
            item: 包含数据的 BaseItem 对象。
            xpath: 用于定位主要内容区域的 XPath 表达式。

        Returns:
            更新后的 BaseItem 对象，如果出错则返回 None。
        '''
        try:
            # 基于传入的 xpath 构建更具体的 xpath
            text_xpath = f"{xpath}//text()"
            attachment_xpath = f"{xpath}//a/@href"

            # 提取文本内容
            text_content = ''.join(response.xpath(text_xpath).getall()).strip()

            # 提取附件链接
            attachment_links = response.xpath(attachment_xpath).getall()

            full_attachment_links = []
            for link in attachment_links:
                if link: # 确保链接不为空
                    # 检查链接是否已经是完整的 URL
                    if link.startswith('http://') or link.startswith('https://'):
                        full_attachment_links.append(link)
                    else:
                        # 将相对路径转换为完整的 URL
                        try:
                            full_link = urljoin(response.url, link)
                            full_attachment_links.append(full_link)
                        except ValueError:
                            # 处理无效的相对链接（可选）
                            self.logger.warning(f"无法解析相对链接: {link} 在 {response.url}")
                            
            # 过滤掉不需要的链接
            full_attachment_links = self.filtered_links(full_attachment_links)

            # 将文本内容和附件链接组合
            item['contents'] = {
                'text': text_content,
                'attachments': full_attachment_links
            }

            return item

        except Exception as e:
            self.logger.error(f"使用 XPath '{xpath}' 解析内容时出错: {e} 在 {response.url}")
            # 根据需要决定是否返回 None 或带有部分数据的 item
            # 为了保持原逻辑，这里返回 None
            return None

    def request_attachment_contents(self,response,item:BaseItem):

        # 下载附件内容并将其添加到item对象中。
        attachment_links = item['contents']['attachments']

        if attachment_links is None:
            return item
            
        # 下载每个附件
        for link in attachment_links:
        
            if link.lower().endswith(".pdf"):

                if 'attachments_pdf' not in item['contents']:
                    item['contents']['attachments_pdf'] = []

                pdf_text = self.request_attachment_pdf(link, response)
                item['contents']['attachments_pdf'].append(pdf_text)

        return item

    def request_attachment_pdf(self, link, response) -> str:
        import requests
        from PyPDF2 import PdfReader
        from io import BytesIO

        try:
            # 将 Scrapy Headers 转换为适合 requests 的字典
            scrapy_headers = response.request.headers
            headers = {}
            for k, v in scrapy_headers.items():
                key = k.decode('utf-8')
                # v 是一个包含字节串的列表，需转换成字符串
                value = ", ".join(x.decode('utf-8') for x in v)
                headers[key] = value
            
            # 提取并拼装 Cookie 
            cookies = {}
            for c in response.request.headers.getlist('Cookie'):
                # 将 bytes 转为 str
                c_str = c.decode('utf-8')
                for pair in c_str.split(';'):
                    k, _, v = pair.strip().partition('=')
                    cookies[k] = v

            # 携带头和 Cookies 发起请求
            r = requests.get(link, timeout=10, headers=headers, cookies=cookies)
            if r.status_code == 200:
                pdf_reader = PdfReader(BytesIO(r.content))
                pages_text = [page.extract_text() or "" for page in pdf_reader.pages]
                return "\n".join(pages_text)
            else:
                self.logger.error(f"Failed to download PDF. Status: {r.status_code}")
                return ""
        except Exception as e:
            self.logger.error(f"Error downloading/reading PDF: {e}")
            return ""

    def filtered_links(self,full_attachment_links):

        filtered_links = [
            self._extract_pdf_url(link)
            for link in full_attachment_links
            if link.lower().endswith((".pdf", ".doc", ".docx", ".xls", ".xlsx"))
        ]
        return filtered_links

    def _extract_pdf_url(self,viewer_url) -> str:
       
        count = viewer_url.count("http") or viewer_url.count("https")

        if count == 1:
            # 仅有一个 http(s) 链接，直接返回
            return viewer_url   
        if count > 1:
            # 有多个 http(s) 链接，解析出后一个
            viewer_url = 'http'+ viewer_url.split("http")[-1]
            
            return viewer_url

    def parse_json(self,response,item:BaseItem)->BaseItem:
        """
        解析JSON格式的响应数据，并将解析后的数据赋值给传入的item的'contents'字段
        
        Args:
            response (Response): 响应对象，其中包含了需要解析的JSON数据
            item (BaseItem): 待填充数据的对象
        
        Returns:
            BaseItem: 填充了JSON数据的item对象，如果解析失败则返回None
        
        Raises:
            无
        
        """
        
        try:
            data = response.json()
            item['contents'] = data
            return item

        except Exception as e:

            logger.error("Parse json error",e)
            return None
        
    # 自动提取url和title
    def auto_extract_url_title(self,node:Selector,res_url)-> tuple:   

        """
        从选择器项中智能提取标题和URL, 适合对象为<a>标签的情况，存在href。标题优先使用title属性，如果title属性为空，则使用元素文本内容。
        
        Args:
            item (Selector): Scrapy选择器对象
            
        Returns:
            tuple: (标题文本, URL) 如果无法提取则返回 (None, None)
        """
        # 尝试找到所有可能的链接元素
        list_elements = node.xpath(".//a")
    
        # 如果没有找到链接元素，返回None
        if not list_elements:
            return None, None
        
        # 存储候选项
        candidates = []
        
        # 处理所有找到的元素
        for element in list_elements:
            # 获取URL
            url = element.attrib.get('href')
            
            # 优先使用title属性作为标题
            title = element.attrib.get('title')
            
            # 如果title属性为空，尝试使用元素文本内容
            if not title or not title.strip():
                title = element.xpath('string(.)').get().strip()
            
            # 规范化标题文本(去除多余空白)
            if title:
                title = re.sub(r'\s+', '', title.strip())

                # 将有效的标题和URL添加到候选项
                if title and url:
                    url = urljoin(res_url, url)  # 确保URL是完整的
                    candidates.append((title, url))
        
        # 如果没有有效候选项，返回None
        if not candidates:
            return None, None
        
        # 如果只有一个候选项，直接返回
        if len(candidates) == 1:
            return candidates[0]
        
        # 有多个候选项，选择标题最长的
        return max(candidates, key=lambda x: len(x[0]))