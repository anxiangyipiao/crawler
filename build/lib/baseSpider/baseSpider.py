import json
from scrapy.exceptions import CloseSpider
import scrapy
from baseSpider.utils.BloomFilter import bloomFilter
from baseSpider.utils.RedisManage import RedisConnectionManager
from datetime import datetime
from baseSpider.items import BaseItem,RequestItem
from scrapy import signals
import logging
import re




logger = logging.getLogger(__name__)

class BaseSpiderObject(scrapy.Spider):

    name = "base"
    start_urls = []

    next_base_urls = ''  # 用于下一页网址拼接
    contents_base_urls = None  # 用于拼接详情页网址
    province = None  # 必填，爬虫省份
    city = None  # 必填，爬虫城市
    county = None  # 选填，爬虫区/县
    site_name = None
    source = None # 网站
    
    timeRange = 0
    crawl_today = datetime.now() # 爬虫开始时间

    insertCount = 0 # 总任务数量
    successCount = 0 # 成功数量

    # insert_urls = [] # 插入的url
    # success_urls = [] # 成功的url
    failed_urls = [] # 失败的url

    max_page = 10 # 最大页数
    init_failed_count = 0 # 初始化失败数量
    max_failures = 10 # 最大失败数量

    # stop_flag = False      # 终止标识

    task_redis_server = RedisConnectionManager.get_connection(db=0) # Redis连接
    

    # 定义要覆盖或添加的设置
    overrides = {
    }

    custom_settings = None
    

    def __init__(self, *args, **kwargs):
        super(BaseSpiderObject, self).__init__(*args, **kwargs)
        self.custom_settings = self.load_custom_settings()
        self.task_redis_server.rpush('running_spiders', self.name)
        logger.info(f'Spider {self.name} started and added to running queue.')

    def load_custom_settings(self):
    
        
        dict = {

                'DOWNLOADER_MIDDLEWARES': {
                    "baseSpider.middlewares.BaseDownloaderMiddleware": 543, 
                    "baseSpider.middlewares.BaseHeaderMiddleware": 1, # 添加请求头
                    "baseSpider.middlewares.PlaywrightMiddleware": 2, # 使用playwright渲染页面
                },
                'ITEM_PIPELINES': {
                    'base_project.pipelines.BasePipeline': 300, # 数据处理管道
                },
                'ROBOTSTXT_OBEY' : False,
                'DOWNLOAD_DELAY': 2,
                'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
                'CONCURRENT_REQUESTS_PER_IP' : 10,
                'RETRY_ENABLED' : True,
                'RETRY_TIMES': 2,


        }

        if self.overrides is not None:

            custom_settings = {
                **self.overrides,
                **dict           
            }

        else:
             custom_settings = dict

        return custom_settings


   
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
            time = datetime.strptime(str(publish_time), '%Y-%m-%d')

        except:

            logger.error("Time format error")

        return time
    
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
        
        try:
            bloomFilter.add(url)
        except:
            logger.error("BloomFilter add error")

    def is_time_stop(self,publishTime:str)->bool:
        """
        判断当前时间是否超过了发布时间所指定的时间限制
        
        Args:
            publishTime (str): 发布时间，格式为"%Y-%m-%d %H:%M:%S"
        
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
            logger.debug(f"No next page or stopping condition met at page {page}.")

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

        # 检查任务是否满足停止条件,如果时间超过timeRange天则跳过
        if self.is_time_stop(task['publish_time']):
            
            self.log("Stopping spider due to time condition.")
            # raise CloseSpider(reason='Time Stop Condition Met')
            return False
 
        # 检查任务是否满足停止条件,如果url已经爬取过则跳过
        if self.is_url_having(task['url']):
            self.log("Url exit.")
            return False

        # 计算任务数量
        try:           
                self.insertCount += 1
                self.failed_urls.append(task['url'])

        except Exception as e:
                
                logger.error("Insert task item error",e)

        return True

    def insert_url_error(self):
        
        try:
            data = {
                'source': self.source,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            self.task_redis_server.lpush('url_error',json.dumps(data))
        
        except:
            logger.error("Insert url queue error")

    def insert_time_error(self):
        
        try:
            data = {
                'source': self.source,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            self.task_redis_server.lpush('time_error',json.dumps(data))
        except:
            logger.error("Insert time queue error")

    def get_key(self):
        return  "task_log:" + self.source + ":" + self.crawl_today.strftime('%Y-%m-%d') + ":" + self.name

    def init_source_log(self,key):
       
        # 参数1 今天网站更新的总数量
        # 参数2 今天网站爬取的成功数量
        # 参数3 今天网站爬取的失败数量
        # 参数4 本次爬取成功的数量 
        # 参数5 本次爬取失败的数量
        # 参数6 今天的日期
        # 参数7 最近一次爬取的时间
        # 参数8 本轮爬虫运行的次数
        # 参数9 今天爬取的次数
        # 参数10 失败的url,存储的是url的列表
        # key 为 source + 日期

        data = {
            'time': self.crawl_today.strftime('%Y-%m-%d'),
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

        # hash 结构存储

        if not self.task_redis_server.exists(key):
                
            self.task_redis_server.hmset(key, data)
       
    def read_source_log(self,key):

        data = self.task_redis_server.hgetall(key)

        # 转为字典
        return {
            'time': data[b'time'].decode('utf-8'),
            'today_all_request': int(data[b'today_all_request'].decode('utf-8')),
            'today_success_request': int(data[b'today_success_request'].decode('utf-8')),
            'today_fail_request': int(data[b'today_fail_request'].decode('utf-8')),
            'this_time_all_request': int(data[b'this_time_all_request'].decode('utf-8')),
            'this_time_success_request': int(data[b'this_time_success_request'].decode('utf-8')),
            'this_time_fail_request': int(data[b'this_time_fail_request'].decode('utf-8')),
            'last_time': data[b'last_time'].decode('utf-8'),
            'run_time': data[b'run_time'].decode('utf-8'),
            'crawl_count': int(data[b'crawl_count'].decode('utf-8')),
            'failed_urls':  json.loads(data[b'failed_urls'].decode('utf-8'))
        }
  
    def write_source_log(self,key,data:dict):
        
        data['failed_urls'] = json.dumps(data['failed_urls'])
        self.task_redis_server.hmset(key, data)

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

        # # 计算今日总请求数量
        # data['all_request'] = data['all_request'] +  self.insertCount -  data['fail_request']

        # # 计算今日成功数量
        # data['success_request'] += self.successCount

        # # 计算今日失败数量
        # data['fail_request'] = data['all_request'] - data['success_request']


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

    def log_info(self,data):
         # 输出日志
        logger.info(
            f"\nthis_time_all_request: { data['this_time_all_request']}, \n" 
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
            if response.xpath('//iframe'):
                # 获取pdf文件地址
                req_url = response.xpath('//iframe/@src').extract_first()
                item['contents'] = req_url
            
            else:
                # 获取html页面内容
                item['contents'] = response.text

            return item

        except Exception as e:

            logger.error("Parse content error",e)
            return None
        
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