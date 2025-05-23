import inspect
import json
import random
import time
import os
from urllib.parse import urljoin
from scrapy.exceptions import CloseSpider
import scrapy
from src.utils.bloom_filter import bloomFilter # Updated import
from src.utils.redis_manager import RedisConnectionManager # Updated import
from datetime import datetime
from src.models.items import BaseItem, RequestItem # Updated import
from scrapy import signals
import logging
import re
from scrapy.selector.unified import Selector

logger = logging.getLogger(__name__)

class SpiderMeta(type):
    def __new__(mcs, name, bases, attrs):
        base_settings = {}
        for base in reversed(bases):
            base_custom = getattr(base, 'custom_settings', None)
            if isinstance(base_custom, dict):
                base_settings.update(base_custom) # Changed from |= to update for broader Python compatibility if needed, though |= is fine for dicts in Py3.9+

        custom_settings = attrs.get('custom_settings', {})
        if not isinstance(custom_settings, dict):
            custom_settings = {}

        merge_keys = ['DOWNLOADER_MIDDLEWARES', 'ITEM_PIPELINES', 'SPIDER_MIDDLEWARES', 'EXTENSIONS']
        merged = base_settings.copy()
        for key, value in custom_settings.items():
            if key in merge_keys and key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = {**merged[key], **value} # More explicit merge, value overwrites merged[key]
            else:
                merged[key] = value

        attrs['custom_settings'] = merged
        return super().__new__(mcs, name, bases, attrs)

class BaseSpider(scrapy.Spider, metaclass=SpiderMeta): # Renamed to BaseSpider for clarity
    name = "base_spider" # Generic name, should be overridden by subclasses
    start_urls = '' # Should be a list or overridden by subclasses

    next_base_urls = ''
    contents_base_urls = None
    province = None
    city = None
    county = None
    site_name = None
    source = None
    page_over = False
    # current_directory = None # This was determined dynamically, might need adjustment or removal if not used broadly

    timeRange = 7
    crawl_today = datetime.now()
    last_publish_time = None
    use_mobile_ua = False

    insertCount = 0
    successCount = 0
    failed_urls = []
    max_page = 2
    init_failed_count = 0
    max_failures = 10

    task_redis_server = None # Initialize in __init__ or from_crawler for clarity and testability

    detail_xpath = '//body'

    # Default custom_settings. Specific spiders can override or extend these.
    # Paths need to point to the new locations within the 'src' directory.
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            "src.middlewares.custom_middlewares.BaseDownloaderMiddleware": 543, # Adjusted path
            "src.middlewares.custom_middlewares.BaseHeaderMiddleware": 542, # Adjusted path & order
            "src.middlewares.custom_middlewares.PlaywrightMiddleware": 541, # Adjusted path & order
            # "src.middlewares.custom_middlewares.BaseRetryMiddleware": 600, # Consider enabling if custom retry is preferred
            # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None, # Disable default if custom is used
        },
        'ITEM_PIPELINES': {
            "src.pipelines.custom_pipelines.BasePipeline": 300, # Adjusted path
        },
        # Other settings from the original file, ensure they are still relevant
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS_PER_IP': 8,
        'RETRY_ENABLED': True, # This enables Scrapy's built-in retry middleware
        'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        'LOG_LEVEL': 'INFO',
        # PLAYWRIGHT_HEADLESS can be set here or in global settings.py
        # 'PLAYWRIGHT_HEADLESS': True, 
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize task_redis_server here if not using from_crawler
        # Ensure Redis connection is properly configured via settings
        if not BaseSpider.task_redis_server:
             # Assuming REDIS_DB for tasks is specified in settings, or use a default
            redis_db_tasks = self.settings.getint('REDIS_DB_TASKS', 0) 
            BaseSpider.task_redis_server = RedisConnectionManager.get_connection(db=redis_db_tasks)

        # Dynamic determination of current_directory might be fragile.
        # If it's for loading spider-specific resources, consider other mechanisms.
        # self.current_directory = ... 

        if not self.source and self.start_urls:
            if isinstance(self.start_urls, (list, tuple)) and self.start_urls:
                self.source = urlparse(self.start_urls[0]).netloc
            elif isinstance(self.start_urls, str):
                self.source = urlparse(self.start_urls).netloc
        
        if self.name != "base_spider": # Avoid base class itself registering as running
            self.task_redis_server.rpush('running_spiders', self.name)
            logger.info(f'Spider {self.name} started and added to running queue.')

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        # Access settings from crawler.settings
        # Example: spider.my_setting = crawler.settings.get('MY_SETTING')
        # Initialize Redis connection here for better management with Scrapy's lifecycle
        if not cls.task_redis_server:
            redis_db_tasks = crawler.settings.getint('REDIS_DB_TASKS', 0) # Get from Scrapy settings
            cls.task_redis_server = RedisConnectionManager.get_connection(db=redis_db_tasks)
        
        crawler.signals.connect(spider.spider_closed_handler, signal=signals.spider_closed)
        # crawler.signals.connect(spider.spider_opened_handler, signal=signals.spider_opened)
        return spider

    # ... (keep get_base_item, is_time_out, extract_number, format_time, format_time_to_str) ...
    # ... (is_url_having, add_url, is_time_stop, has_next_page, request_next_page) ...
    # ... (update_publish_time, calculate_task_item, update_state, insert_url_error, insert_time_error) ...
    # ... (get_key, init_source_log, read_source_log, write_source_log, check_member_exists) ...
    # ... (insert_task_log, compare_time, log_info) ...

    # Renamed original closed method to avoid conflict with scrapy.Spider.closed signal handler
    def spider_closed_handler(self, reason):
        logger.info(f"Spider {self.name} closed, reason: {reason}")
        self.insert_task_log() # Call the original logging logic
        if self.name != "base_spider":
            self.task_redis_server.lrem('running_spiders', 0, self.name)
            logger.info(f'Spider {self.name} removed from running queue.')

    # ... (keep parse_task, parse, parse_content_detal, errback_httpbin) ...
    # ... (parse_content, determine_response_type, parse_html, parse_contents_with_xpath) ...
    # ... (request_attachment_contents, request_attachment_pdf, filtered_links, _extract_pdf_url, parse_json, auto_extract_url_title) ...

    # Ensure all helper methods like format_time, is_url_having etc. use self.task_redis_server or pass it if needed.
    # For example, is_url_having uses bloomFilter which itself uses Redis.

    # Make sure PyPDF2 and other specific dependencies are in requirements.txt
    # The request_attachment_pdf method uses requests and PyPDF2.

    # Helper methods like get_base_item, format_time, etc., remain largely the same
    # but ensure they use updated class attributes or passed parameters correctly.

    def get_base_item(self) -> BaseItem:
        baseItem = BaseItem()
        baseItem['source'] = self.source
        baseItem['site_name'] = self.site_name
        baseItem['province'] = self.province
        baseItem['city'] = self.city
        baseItem['county'] = self.county
        return baseItem

    def is_time_out(self, time_obj: datetime) -> bool:
        if not isinstance(time_obj, datetime):
            logger.warning(f"is_time_out received non-datetime object: {time_obj}")
            return True # Or handle as an error
        return abs((time_obj.date() - self.crawl_today.date()).days) > self.timeRange

    def extract_number(self, string: str) -> str | None:
        if not isinstance(string, str):
            return None
        match = re.search(r'\d{4}-\d{2}-\d{2}', string)
        return match.group() if match else None

    def format_time(self, publish_time_str: str) -> datetime | None:
        try:
            return datetime.strptime(str(publish_time_str), '%Y-%m-%d')
        except (ValueError, TypeError) as e:
            logger.error(f"Time format error for '{publish_time_str}': {e}")
            return None

    def format_time_to_str(self, publish_time: str) -> str | None:
        if not isinstance(publish_time, str):
            return None
        # Simplified replacements
        publish_time = re.sub(r'[()/\[\]年月.]', '-', publish_time)
        publish_time = publish_time.replace('日', '').replace(' ', '')
        publish_time = self.extract_number(publish_time) # Extracts YYYY-MM-DD
        return publish_time[:10] if publish_time and len(publish_time) >= 10 else publish_time

    def is_url_having(self, url: str) -> bool:
        if not url:
            return False # Or True, depending on desired behavior for empty URLs
        return bloomFilter.is_contained(url)

    def add_url(self, url: str):
        if url:
            bloomFilter.add(url)

    def is_time_stop(self, publish_time_str: str) -> bool:
        time_obj = self.format_time(publish_time_str)
        if not time_obj:
            return True # If time cannot be parsed, consider it as a stop condition
        return self.is_time_out(time_obj)

    def has_next_page(self, baseItem: BaseItem, page: int) -> bool:
        if self.page_over: # If page_over is already true, no next page
            return False
        if not baseItem.get('publish_time'):
             # If last item has no publish time, logic for stopping based on time might be tricky.
             # Defaulting to True to continue if max_page not reached, or False to stop.
             # This depends on the specific spider's logic if publish_time is not always available.
            logger.warning("has_next_page: publish_time not found in baseItem. Pagination behavior might be affected.")
            return page < self.max_page # Continue if max_page not reached

        return not self.is_time_stop(baseItem['publish_time']) and page < self.max_page

    def request_next_page(self, baseItem, page, request_params):
        if self.has_next_page(baseItem, page):
            logger.debug(f"Requesting next page: {page + 1}") # page is current, next is page + 1
            # Ensure request_params['meta'] exists if you plan to update it
            if 'meta' not in request_params or request_params['meta'] is None:
                request_params['meta'] = {}
            request_params['meta']['page'] = page + 1 # Pass next page number in meta
            return self.parse_task(RequestItem(**request_params))
        else:
            self.page_over = True
            logger.info(f"No next page or stopping condition met at page {page}.")
            return None # Explicitly return None

    def update_publish_time(self, publish_time_str: str):
        new_publish_time = self.format_time(publish_time_str)
        if new_publish_time:
            if self.last_publish_time is None or new_publish_time > self.last_publish_time:
                self.last_publish_time = new_publish_time

    def calculate_task_item(self, task: BaseItem) -> bool:
        if not task.get('url'):
            self.insert_url_error()
            logger.error('URL is missing in the task item. Spider might close.')
            # raise CloseSpider('url_missing') # Consider if this should always close the spider
            return False
        if not task.get('publish_time'):
            self.insert_time_error()
            logger.error('Publish time is missing in the task item. Spider might close.')
            # raise CloseSpider('publish_time_missing')
            return False

        self.update_publish_time(task['publish_time'])

        if self.is_time_stop(task['publish_time']):
            logger.debug(f"Item from {task['url']} with time {task['publish_time']} is out of range. Skipping.")
            return False

        if self.is_url_having(task['url']):
            logger.debug(f"URL {task['url']} already processed (found in Bloom filter). Skipping.")
            return False

        self.insertCount += 1
        self.failed_urls.append(task['url'])
        return True

    def update_state(self) -> bool:
        # This condition means all fetched items that were added to insertCount
        # have been successfully processed (successCount matched insertCount)
        # AND pagination has completed (page_over is True).
        return self.insertCount == self.successCount and self.page_over

    def insert_url_error(self):
        try:
            data = {
                'source': self.source or self.name, # Fallback to spider name if source is not set
                'name': self.name,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            self.task_redis_server.lpush('url_error', json.dumps(data))
        except Exception as e:
            logger.error(f"Insert URL error to Redis queue failed: {e}")

    def insert_time_error(self):
        try:
            data = {
                'source': self.source or self.name,
                'name': self.name,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            self.task_redis_server.lpush('time_error', json.dumps(data))
        except Exception as e:
            logger.error(f"Insert time error to Redis queue failed: {e}")

    def get_key(self) -> str:
        return f"task_log:{self.crawl_today.strftime('%Y-%m-%d')}:{self.source or 'unknown_source'}:{self.name}"

    def init_source_log(self, key: str):
        if not self.task_redis_server.exists(key):
            data = {
                'name': self.name,
                'source': self.source or 'unknown_source',
                'site_name': self.site_name or 'unknown_site',
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
            self.task_redis_server.hmset(key, data)

    def read_source_log(self, key: str) -> dict | None:
        if not self.task_redis_server.exists(key):
            return None
        data = self.task_redis_server.hgetall(key)
        return {
            'name': data.get('name'),
            'source': data.get('source'),
            'site_name': data.get('site_name'),
            'state': data.get('state', 'failure'), # Default state
            'last_publish_time': data.get('last_publish_time', ''),
            'today_all_request': int(data.get('today_all_request', 0)),
            'today_success_request': int(data.get('today_success_request', 0)),
            'today_fail_request': int(data.get('today_fail_request', 0)),
            'this_time_all_request': int(data.get('this_time_all_request', 0)),
            'this_time_success_request': int(data.get('this_time_success_request', 0)),
            'this_time_fail_request': int(data.get('this_time_fail_request', 0)),
            'last_time': data.get('last_time', ''),
            'run_time': data.get('run_time', ''),
            'crawl_count': int(data.get('crawl_count', 0)),
            'failed_urls': json.loads(data.get('failed_urls', '[]'))
        }

    def write_source_log(self, key: str, data: dict):
        try:
            # Ensure all values are appropriate for hmset (strings or numbers)
            log_data_to_write = {k: (json.dumps(v) if isinstance(v, (list, dict)) else str(v)) for k, v in data.items()}
            self.task_redis_server.hmset(key, log_data_to_write)
            score = datetime.now().timestamp()
            # Using zadd with xx=True updates only if member exists, nx=True adds only if member does not exist.
            # Simple zadd will add or update.
            self.task_redis_server.zadd('key_sorted_set', {key: score})
        except Exception as e:
            logger.error(f"Error writing source log to Redis for key {key}: {e}")

    def check_member_exists(self, key: str) -> bool:
        return self.task_redis_server.zscore('key_sorted_set', key) is not None

    def insert_task_log(self):
        key = self.get_key()
        self.init_source_log(key)
        log_data = self.read_source_log(key)
        if not log_data: # If log data couldn't be read, abort
            logger.error(f"Could not read source log for key {key}. Aborting insert_task_log.")
            return

        log_data['state'] = 'success' if self.update_state() else 'failure'
        # log_data['current_directory'] = self.current_directory # Re-evaluate if this is needed
        log_data['this_time_all_request'] = self.insertCount
        log_data['this_time_success_request'] = self.successCount
        log_data['this_time_fail_request'] = self.insertCount - self.successCount

        # today_all_request should sum up all items ever intended for today, 
        # not just sum of this_time_all_request from multiple runs if they overlap.
        # This logic might need refinement based on how 'today_all_request' is defined.
        # Assuming it's total unique items processed or attempted today.
        # A safer way might be to increment by new items from this run.
        log_data['today_all_request'] = log_data.get('today_all_request',0) + self.insertCount
        log_data['today_success_request'] = log_data.get('today_success_request',0) + self.successCount
        log_data['today_fail_request'] = log_data['today_all_request'] - log_data['today_success_request']

        log_data['last_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_data['run_time'] = str((datetime.now() - self.crawl_today).total_seconds()) # Use total_seconds for precision

        if self.last_publish_time and self.compare_time(log_data.get('last_publish_time')):
            log_data['last_publish_time'] = self.last_publish_time.strftime('%Y-%m-%d')
        
        log_data['crawl_count'] = log_data.get('crawl_count', 0) + 1
        log_data['failed_urls'] = self.failed_urls # This should be a list of URLs that failed in *this* run
        # Or, if it's cumulative for the day, it needs different logic.

        self.write_source_log(key, log_data)
        self.log_info(log_data)

    def compare_time(self, time_str: str) -> bool:
        if self.last_publish_time is None:
            return False
        if not time_str:
            return True
        try:
            datetime_object = datetime.strptime(time_str, '%Y-%m-%d')
            return self.last_publish_time.date() > datetime_object.date()
        except ValueError:
            logger.warning(f"Could not parse time_str '{time_str}' in compare_time.")
            return True # Or False, depending on desired behavior for unparseable time

    def log_info(self, data: dict):
        log_message_parts = [f"{k}: {v}" for k, v in data.items()]
        logger.info("Spider Run Summary:\n" + "\n".join(log_message_parts))

    def parse_task(self, task_item: RequestItem):
        # Random delay
        # time.sleep(random.uniform(0.5, 1.5)) # More granular sleep

        method = task_item.get('method', 'GET').upper()
        url = task_item.get('url')
        callback = task_item.get('callback', self.parse) # Default to self.parse if not specified
        errback = task_item.get('errback', self.errback_httpbin)
        meta = task_item.get('meta')
        cookies = task_item.get('cookies')
        headers = task_item.get('headers')
        params = task_item.get('params') # For GET query params or POST body
        request_body_type = task_item.get('request_body', 'json').lower() # For POST: formdata or json

        if not url:
            logger.error("RequestItem missing URL.")
            return None

        request_args = {
            'url': url,
            'callback': callback,
            'errback': errback,
            'dont_filter': task_item.get('dont_filter', True),
            'meta': meta,
            'cookies': cookies,
            'headers': headers
        }

        if method == 'GET':
            # Scrapy handles GET params directly in URL or via Request(url, body=urlencode(params)) for specific cases
            # If params are meant as query string, they should be part of the URL or handled by a middleware
            # The original code used body=json.dumps(params) for GET, which is unusual.
            # Assuming params for GET are query parameters, they should be encoded into the URL.
            # If they were intended for a GET request with a body (non-standard), then body=json.dumps(params) is correct.
            if params:
                 # If params are for query string, they should be added to URL. For now, keeping original logic if body was intended.
                 # request_args['body'] = json.dumps(params) # Original logic
                 logger.warning("Params provided for GET request. If they are query parameters, they should be in the URL.")
            return scrapy.Request(method='GET', **request_args)

        elif method == 'POST':
            request_args['method'] = 'POST'
            if request_body_type == 'formdata':
                request_args['formdata'] = params
                return scrapy.FormRequest(**request_args)
            elif request_body_type == 'json':
                request_args['body'] = json.dumps(params)
                return scrapy.Request(**request_args)
            else:
                logger.warning(f"Unsupported request_body type: {request_body_type} for POST. Defaulting to JSON.")
                request_args['body'] = json.dumps(params)
                return scrapy.Request(**request_args)
        else:
            logger.error(f"Unsupported HTTP method: {method}")
            return None

    def parse(self, response, **kwargs):
        # This method should be implemented by subclasses to extract data from the initial response(s).
        self.logger.info(f"Visited {response.url}. Subclass should implement parse method.")
        # Example: yield from self.parse_list_page(response)
        pass

    def parse_content_detal(self, response):
        item = self.parse_content(response)
        if item:
            yield item

    def errback_httpbin(self, failure):
        self.init_failed_count += 1
        logger.error(f"Request failed for {failure.request.url if failure.request else 'Unknown URL'}: {failure.value} (Total failures for this spider instance: {self.init_failed_count})")

        # Accessing spider from failure object if needed: failure.request.meta.get('spider')
        # Or ensure spider instance is available via self

        if self.init_failed_count > self.max_failures:
            logger.error(f"Maximum number of failures ({self.max_failures}) reached for spider {self.name}. Stopping spider.")
            # This will call the spider_closed_handler via Scrapy signals
            raise CloseSpider(f'max_failures_reached_{self.name}')

    def parse_content(self, response) -> BaseItem | None:
        item = response.meta.get('item')
        if not item:
            logger.warning(f"No item found in response.meta for {response.url}. Cannot parse content.")
            return None

        content_type = response.headers.get('Content-Type', b'').decode('utf-8').lower()

        if 'json' in content_type:
            return self.parse_json(response, item)
        elif 'html' in content_type or not content_type: # Default to HTML if no content-type or it's HTML
            return self.parse_html(response, item)
        else:
            logger.warning(f"Unhandled content type '{content_type}' for {response.url}. Attempting to determine type.")
            return self.determine_response_type(response, item)

    def determine_response_type(self, response, item: BaseItem) -> BaseItem | None:
        try:
            json.loads(response.text) # Check if it's valid JSON
            return self.parse_json(response, item)
        except json.JSONDecodeError:
            return self.parse_html(response, item) # Fallback to HTML
        except Exception as e:
            logger.error(f"Error determining response type for {response.url}: {e}")
            return item # Return item as is, or None

    def parse_html(self, response, item: BaseItem) -> BaseItem | None:
        try:
            item = self.parse_contents_with_xpath(response, item, self.detail_xpath)
            if item: # Only proceed if parse_contents_with_xpath was successful
                item = self.request_attachment_contents(response, item)
            return item
        except Exception as e:
            logger.error(f"Parse HTML content error for {response.url}: {e}", exc_info=True)
            return item # Return item, possibly partially filled, or None

    def parse_contents_with_xpath(self, response, item: BaseItem, xpath: str) -> BaseItem | None:
        try:
            text_xpath = f"{xpath}//text()"
            attachment_xpath = f"{xpath}//a/@href"

            text_content_list = response.xpath(text_xpath).getall()
            text_content = ' '.join(text.strip() for text in text_content_list if text.strip()).strip()
            text_content = re.sub(r'\s+', ' ', text_content) # Normalize whitespace

            attachment_links = response.xpath(attachment_xpath).getall()
            full_attachment_links = []
            for link in attachment_links:
                if link:
                    try:
                        full_link = response.urljoin(link) # Use response.urljoin for robust relative URL resolution
                        full_attachment_links.append(full_link)
                    except ValueError:
                        self.logger.warning(f"Could not parse relative link: {link} on page {response.url}")
            
            filtered_attachment_links = self.filtered_links(full_attachment_links)

            if 'contents' not in item or not isinstance(item['contents'], dict):
                 item['contents'] = {} # Initialize if not present or wrong type

            item['contents']['text'] = text_content
            item['contents']['attachments'] = filtered_attachment_links
            return item
        except Exception as e:
            self.logger.error(f"Error parsing content with XPath '{xpath}' for {response.url}: {e}", exc_info=True)
            return item # Return item as is or None

    def request_attachment_contents(self, response, item: BaseItem) -> BaseItem:
        if not item.get('contents') or not item['contents'].get('attachments'):
            return item

        attachment_links = item['contents']['attachments']
        pdf_texts = []
        for link in attachment_links:
            # This check should ideally be in filtered_links or based on a more robust type detection
            if link.lower().endswith(".pdf"):
                pdf_text = self.request_attachment_pdf(link, response)
                if pdf_text:
                    pdf_texts.append({'url': link, 'text': pdf_text})
        
        if pdf_texts:
            item['contents']['attachments_pdf'] = pdf_texts # Store as list of dicts
        return item

    def request_attachment_pdf(self, link: str, response) -> str | None:
        # Ensure PyPDF2 is installed and imported at the top of the file or within the method if preferred.
        # import requests # Already imported at top
        from PyPDF2 import PdfReader # Consider moving to top if always used
        from io import BytesIO

        try:
            # Using Scrapy's request mechanism for downloading PDFs is generally preferred
            # to leverage Scrapy's downloader middlewares, retry policies, etc.
            # However, the original code uses `requests`. If sticking with `requests`:
            scrapy_headers = response.request.headers
            headers = {k.decode(): v[0].decode() for k, v in scrapy_headers.items() if v} # Simplified header conversion
            
            # Cookies from the original request that led to this PDF link
            # This might not be the correct set of cookies for the PDF link itself.
            # cookies = response.request.cookies 

            # It's better to yield a new scrapy.Request for the PDF and parse its response.
            # For now, sticking to the original direct `requests` call with caution:
            pdf_response = requests.get(link, timeout=20, headers=headers, stream=True) # Increased timeout, use stream
            pdf_response.raise_for_status()

            if 'application/pdf' not in pdf_response.headers.get('Content-Type', '').lower():
                self.logger.warning(f"Link {link} did not return a PDF content-type.")
                return None

            pdf_file = BytesIO(pdf_response.content)
            pdf_reader = PdfReader(pdf_file)
            pages_text = [page.extract_text() or "" for page in pdf_reader.pages]
            return "\n".join(pages_text).strip()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to download PDF from {link}: {e}")
        except Exception as e:
            self.logger.error(f"Error reading PDF from {link}: {e}", exc_info=True)
        return None

    def filtered_links(self, full_attachment_links: list) -> list:
        # Filters and potentially transforms attachment links.
        # Original logic also called _extract_pdf_url, which seemed to handle multiple http in URL.
        valid_extensions = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip", ".rar", ".txt", ".csv") # Expanded list
        processed_links = []
        for link in full_attachment_links:
            if isinstance(link, str) and link.lower().endswith(valid_extensions):
                # The _extract_pdf_url logic might be specific and needs review if it's generally applicable.
                # For now, just adding the link if it has a valid extension.
                # extracted_link = self._extract_pdf_url(link) 
                # processed_links.append(extracted_link)
                processed_links.append(link)
        return list(set(processed_links)) # Remove duplicates

    def _extract_pdf_url(self, viewer_url: str) -> str:
        # This method seems to handle cases where a URL might be embedded within another, e.g., a viewer URL.
        # It extracts the last http(s) part.
        if not isinstance(viewer_url, str):
            return viewer_url
        
        parts = re.split(r'(https?://)', viewer_url)
        if len(parts) > 2: # More than one http(s):// found
            # Reconstruct the last URL: parts[-2] is the last 'http://' or 'https://', parts[-1] is the rest of the URL.
            return parts[-2] + parts[-1]
        return viewer_url # Only one or no http(s) found, return as is

    def parse_json(self, response, item: BaseItem) -> BaseItem | None:
        try:
            data = response.json()
            # It's generally better to map specific fields from JSON to item fields
            # rather than assigning the whole JSON to item['contents'].
            # For now, keeping original behavior.
            if 'contents' not in item or not isinstance(item['contents'], dict):
                 item['contents'] = {} # Initialize if not present or wrong type
            item['contents']['json_data'] = data # Store under a specific key
            # Or, if the JSON structure is known and maps to item fields:
            # item['title'] = data.get('title')
            # item['body_text'] = data.get('content')
            return item
        except json.JSONDecodeError as e:
            logger.error(f"Parse JSON error for {response.url}: {e}. Response text: {response.text[:200]}...")
        except Exception as e:
            logger.error(f"Unexpected error parsing JSON for {response.url}: {e}", exc_info=True)
        return item # Return item as is or None

    def auto_extract_url_title(self, node: Selector, response_url: str) -> tuple[str | None, str | None]:
        candidates = []
        # Look for <a> tags directly under the node or deeply nested
        for element in node.xpath(".//a[@href]"): # Ensure href exists
            url = element.attrib.get('href')
            title = element.attrib.get('title')

            if not title or not title.strip():
                # Extract all text within the <a> tag, join, and strip
                title_parts = element.xpath(".//text()").getall()
                title = ' '.join(part.strip() for part in title_parts if part.strip()).strip()
                title = re.sub(r'\s+', ' ', title) # Normalize whitespace
            
            if title and url:
                try:
                    full_url = response_urljoin(response_url, url) # Use Scrapy's urljoin
                    candidates.append((title, full_url))
                except ValueError:
                    self.logger.warning(f"Could not join URL: base='{response_url}', relative='{url}'")

        if not candidates:
            return None, None
        if len(candidates) == 1:
            return candidates[0]
        
        # Prefer candidates where title is not just the URL itself (if URL is also text)
        # Then, prefer longer titles as a heuristic for more descriptive titles.
        # This can be made more sophisticated.
        return max(candidates, key=lambda x: (x[0] != x[1], len(x[0])))

# Helper function from scrapy.utils.url, not directly available, so using urllib.parse.urljoin
# or response.urljoin if a response object is available.
from urllib.parse import urljoin as response_urljoin # Alias for clarity in auto_extract_url_title
from urllib.parse import urlparse # For __init__ source determination
