# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import json
import requests
from scrapy import signals
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter # Ensure itemadapter is in requirements.txt
from fake_useragent import UserAgent # Ensure fake_useragent is in requirements.txt
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import logging
from scrapy.http import HtmlResponse
from scrapy.utils.defer import deferred_from_coro
from scrapy.exceptions import IgnoreRequest
from playwright.async_api import async_playwright # Ensure playwright is in requirements.txt

# It's good practice to ensure all external libraries are listed in requirements.txt

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

        # Consider removing print or using logger for debugging
        # print('BaseDownloaderMiddleware process_request') 
        logger.debug('BaseDownloaderMiddleware process_request for %s', request.url)

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
        logger.error("Error processing request %s: %s", request.url, exception)
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BaseHeaderMiddleware:
    
    def process_request(self, request, spider):
        # Ensure User-Agent is a string, not bytes, if comparing or manipulating as string
        user_agent_header = request.headers.get('User-Agent')
        current_ua_str = user_agent_header.decode() if isinstance(user_agent_header, bytes) else user_agent_header

        if current_ua_str is None or "Scrapy" in current_ua_str:
            if getattr(spider, 'use_mobile_ua', False): 
                ua = UserAgent(platforms='mobile', use_cache_server=False) # Added use_cache_server=False for robustness
                request.headers['User-Agent'] = ua.random
            else:
                ua = UserAgent(platforms='desktop', use_cache_server=False) # Added use_cache_server=False
                request.headers['User-Agent'] = ua.random
   
        return None

class PlaywrightMiddleware:
    def __init__(self):
        self.playwright = None
        self.browser = None
        # Consider making headless configurable via settings
        self.headless = True # Default to True, can be overridden by spider attribute or settings

    async def _initialize(self, spider):
        if not self.playwright:
            self.playwright = await async_playwright().start()
            # Allow spider to specify headless mode
            self.headless = getattr(spider, 'playwright_headless', self.headless)
            self.browser = await self.playwright.chromium.launch(headless=self.headless)

    async def _block_resources(self, page):
        # Resource types to allow, can be made configurable
        allowed_resource_types = ["document", "script", "xhr", "fetch"]
        await page.route("**/*", lambda route: route.continue_() if route.request.resource_type in allowed_resource_types else route.abort())

    async def _process_request(self, request, spider):
        if not request.meta.get('use_playwright'):
            return None

        logger.debug('PlaywrightMiddleware processing request %s', request.url)
        await self._initialize(spider)
        page = await self.browser.new_page()
        
        # Apply stealth script if provided by spider or settings
        stealth_js_path = getattr(spider, 'playwright_stealth_path', request.meta.get('stealth_path'))
        if stealth_js_path:
            try:
                with open(stealth_js_path, 'r') as f:
                    await page.add_init_script(f.read())
            except Exception as e:
                logger.warning(f"Could not apply stealth.js from {stealth_js_path}: {e}")

        if request.meta.get('block_resources', True): # Allow disabling resource blocking
             await self._block_resources(page)

        try:
            await page.goto(request.url, timeout=request.meta.get('playwright_timeout', 60000)) # Configurable timeout
            content = await page.content()
        except Exception as e:
            logger.error(f"Playwright error for {request.url}: {e}")
            await page.close()
            raise IgnoreRequest(f"Playwright error: {e}") # Or return a specific response/retry
        
        await page.close()

        return HtmlResponse(
            request.url,
            body=content.encode('utf-8'), 
            encoding='utf-8',
            request=request
        )

    def process_request(self, request, spider):
        if request.meta.get('use_playwright'):
            return deferred_from_coro(self._process_request(request, spider))
        return None

    async def _close_resources(self):
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        # Pass settings to middleware if needed, e.g. for headless config
        middleware.headless = crawler.settings.getbool('PLAYWRIGHT_HEADLESS', True)
        return middleware

    def spider_closed(self, spider):
        # Ensure cleanup is called correctly
        return deferred_from_coro(self._close_resources())


class BaseRetryMiddleware(RetryMiddleware):
    # Consider if this custom retry middleware is still needed or if Scrapy's default with proper settings is enough
    # Default Scrapy RetryMiddleware already handles many cases and proxying via meta['proxy']

    # EXCEPTIONS_TO_RETRY is already defined in the parent class, can be extended if needed
    # Default: (defer.TimeoutError, TimeoutError, DNSLookupError,
    #           ConnectionRefusedError, ConnectionDone, ConnectError, ConnectionLost,
    #           TCPTimedOutError, ResponseFailed, TunnelError)

    def __init__(self, settings):
        super().__init__(settings) # Initializes RETRY_HTTP_CODES, max_retry_times etc.
        # PROXY_URL and PROXY_TOKEN specific to this custom middleware
        self.proxy_url = settings.get('PROXY_URL') 
        self.proxy_token = settings.get('PROXY_TOKEN')
        self.proxy_headers = {
            'token': self.proxy_token,
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)', # Consider making this configurable
        }
        # Ensure this list is populated from settings if you intend to override parent
        # self.RETRY_HTTP_CODES = set(settings.getlist('RETRY_HTTP_CODES')) 

    # process_response and process_exception can often be inherited if the main logic is about _retry
    # The parent class already handles response.status in self.RETRY_HTTP_CODES
    # and exception in self.EXCEPTIONS_TO_RETRY

    def _retry(self, request, reason, spider):
        # Call super()._retry for basic retry logic, then add custom proxy logic
        retryreq = super()._retry(request, reason, spider)
        if retryreq and self.proxy_url: # Only add proxy if retry is happening and proxy_url is set
            proxy = self.get_proxy()
            if proxy:
                # Scrapy expects proxy in meta as 'http://user:pass@host:port'
                # The self.get_proxy() returns a dict {"http": "http://ip:port", "https": "http://ip:port"}
                # Need to pick one and format it, or ensure the proxy service returns it in the correct string format
                # Assuming the proxy service returns a simple ip:port string for the value of 'process'
                if isinstance(proxy, dict) and proxy.get('http'): # Using http proxy from the dict
                    retryreq.meta['proxy'] = proxy['http']
                elif isinstance(proxy, str): # If get_proxy directly returns the string
                     retryreq.meta['proxy'] = proxy 
                logger.debug(f"Retrying {retryreq.url} with proxy {retryreq.meta.get('proxy')}")
            else:
                logger.warning(f"Failed to get proxy for retrying {retryreq.url}")
        return retryreq

    def get_proxy(self):
        if not self.proxy_url or not self.proxy_token:
            logger.warning("PROXY_URL or PROXY_TOKEN not configured for BaseRetryMiddleware")
            return None
        try:
            response = requests.post(self.proxy_url, headers=self.proxy_headers, timeout=5) # Added timeout
            response.raise_for_status()
            body = response.json() # Use .json() for direct dict conversion
            # Ensure 'data' and the actual proxy string exist
            proxy_data = body.get('data')
            if proxy_data:
                # Assuming proxy_data is the ip:port string or similar that can be prefixed with http://
                # Standard Scrapy proxy format: http://user:password@host:port or http://host:port
                return f"http://{proxy_data}" # Construct the proxy string for Scrapy
            else:
                logger.warning(f"Proxy service response did not contain 'data': {body}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get proxy from {self.proxy_url}: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode proxy response from {self.proxy_url}: {e}. Response text: {response.text if 'response' in locals() else 'N/A'}")
            return None
