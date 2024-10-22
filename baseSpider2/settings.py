# Scrapy settings for base project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "baseSpider2"

SPIDER_MODULES = ["baseSpider2.spiders"]
NEWSPIDER_MODULE = "baseSpider2.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "base (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# 设置每个域名的最大并发请求数量
CONCURRENT_REQUESTS_PER_DOMAIN = 10

# 或者设置每个IP地址的最大并发请求数量
CONCURRENT_REQUESTS_PER_IP = 10

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32
# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "base.middlewares.BaseSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   "baseSpider2.middlewares.BaseDownloaderMiddleware": 543, 
   "baseSpider2.middlewares.BaseHeaderMiddleware": 1, # 添加请求头
   "baseSpider2.middlewares.PlaywrightMiddleware": 2, # 使用playwright渲染页面
   # "base.middlewares.BaseRetryMiddleware": 2, # 重试

}

RETRY_ENABLED = True  # 启用重试
RETRY_TIMES = 2 # 最大重试次数
# RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]  # 需要重试的HTTP状态码
# RETRY_PRIORITY_ADJUST = -1

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "baseSpider2.pipelines.BasePipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


# redis
REDIS_HOST = "43.128.136.204"
REDIS_PORT = 16379
REDIS_DB = 0

# rabbitmq
RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "<PASSWORD>"
RABBITMQ_VHOST = "/"
RABBITMQ_EXCHANGE = ""

# mysql
MYSQL_HOST = "58.213.106.158"
MYSQL_PORT = 36000
MYSQL_USER = "bidspider2"
MYSQL_PASSWORD = "cSFbhtFencqH3knm"
MYSQL_DB = "bidSpider2"



# bloomfilter
# 用于布隆过滤器的redis key
BLOOMFILTER_KEY = "bloomfilter"

# info-level 输出日志，debug-level 不输出日志
LOG_LEVEL = "INFO"


