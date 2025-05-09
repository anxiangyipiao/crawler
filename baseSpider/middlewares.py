# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import json
import requests
from scrapy import signals
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import logging
from scrapy.http import HtmlResponse
from scrapy.utils.defer import deferred_from_coro
from scrapy.exceptions import IgnoreRequest
from playwright.async_api import async_playwright


logger = logging.getLogger(__name__)


class BaseSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BaseDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        print('BaseDownloaderMiddleware process_request')

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BaseHeaderMiddleware:
    
    def process_request(self, request, spider):

        if request.headers.get('User-Agent') is None or "Scrapy" in request.headers.get('User-Agent').decode():
            # 检查是否需要使用移动端 User-Agent
            if self.should_use_mobile_ua(request, spider):
                ua = UserAgent(platforms='mobile')
                request.headers['User-Agent'] = ua.random # 移动端UA
            else:
                ua = UserAgent(platforms='desktop')
                request.headers['User-Agent'] = ua.random # 桌面UA
   
        return None

    def should_use_mobile_ua(self, request, spider):
        # 在这里添加你的判断逻辑
        # 例如，可以根据 URL 或 Spider 名称来判断
        # 下面是一个示例，如果 URL 包含 "mobile"，则使用移动端 UA
        
        if spider.get('use_mobile_ua', False) == True:
            return True
    


class PlaywrightMiddleware:
    def __init__(self):
        self.playwright = None
        self.browser = None

    async def _initialize(self):
        if not self.playwright:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)  # 无头模式

    async def _block_resources(self, page):
        await page.route("**/*", lambda route: route.continue_() if route.request.resource_type in ["document", "script", "xhr", "fetch"] else route.abort())

    async def _process_request(self, request, spider):

        print('PlaywrightMiddleware process_request')

        if not request.meta.get('use_playwright'):
            return None

        await self._initialize()
        page = await self.browser.new_page()
        await self._block_resources(page)
        await page.goto(request.url)
        content = await page.content()
        await page.close()

        return HtmlResponse(
            request.url,
            body=content.encode('utf-8'), 
            encoding='utf-8',
            request=request
        )

    def process_request(self, request, spider):
        return deferred_from_coro(self._process_request(request, spider))

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    async def spider_closed(self, spider):
        await self.close()


class BaseRetryMiddleware(RetryMiddleware):

    EXCEPTIONS_TO_RETRY = (TimeoutError,
                           ConnectionRefusedError,
                           IOError, ValueError)

    def __init__(self, settings):
        super().__init__(settings)
        self.RETRY_HTTP_CODES = set(settings.getlist('RETRY_HTTP_CODES'))
        self.max_retry_times = settings.getint('RETRY_TIMES')
        self.proxy_url = settings.get('PROXY_URL')  # 从 settings 中获取
        self.proxy_token = settings.get('PROXY_TOKEN')
        self.proxy_headers = {
            'token': self.proxy_token,
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        }

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            logger.info("Ignoring %s: %s", request, response.status)
            return response

        if response.status in self.RETRY_HTTP_CODES:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response

        return response

    def process_exception(self, request, exception, spider):
        if request.meta.get('dont_retry', False):
            logger.info("Ignoring %s: %s", request, exception)
            return None

        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            logger.info("Retrying %s due to %s", request.url, exception)
            return self._retry(request, exception, spider)
        else:
            return None  # 确保返回 None

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        if retries <= self.max_retry_times:
            logger.info("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True

            # 添加代理支持
            proxy = self.get_proxy()
            if proxy:
                retryreq.meta['proxy'] = proxy

            return retryreq
        else:
            logger.info("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})

    def get_proxy(self):
        try:
            response = requests.post(self.proxy_url, headers=self.proxy_headers)
            response.raise_for_status()  # 检查状态码
            body = json.loads(response.text)
            process = body['data']
            proxies = {
                "http": f"http://{process}",  # HTTP代理
                "https": f"http://{process}",  # HTTPS代理
            }
            return proxies
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to get proxy: {e}")
            return None
