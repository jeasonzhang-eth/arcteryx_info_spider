# Scrapy settings for LuxuryInfoSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
from datetime import datetime

BOT_NAME = "LuxuryInfoSpider"

SPIDER_MODULES = ["LuxuryInfoSpider.spiders"]
NEWSPIDER_MODULE = "LuxuryInfoSpider.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "LuxuryInfoSpider (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "LuxuryInfoSpider.middlewares.LuxuryInfoSpiderSpiderMiddleware": 543,
# }
# DOWNLOAD_HANDLERS = {
#     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
# }

# PLAYWRIGHT_LAUNCH_OPTIONS = {
#     "headless": True
# }
# PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = (
#     30 * 1000
# )
#
# PLAYWRIGHT_BROWSER_TYPE = "chromium"

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # "LuxuryInfoSpider.middlewares.RandomUserAgentMiddleware": 543,
   # "LuxuryInfoSpider.middlewares.RandomProxyMiddleware": 544,
   # "LuxuryInfoSpider.middlewares.ErrorHandlingMiddleware": 545,
   # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None
   # "scrapy_cloudflare_middleware.middlewares.CloudFlareMiddleware": 560,
   # "LuxuryInfoSpider.middlewares.DelayMiddleware": 545,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "LuxuryInfoSpider.pipelines.RedisPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Configure the Redis connection
REDIS_HOST = "130.162.145.124"
REDIS_PORT = 16379
REDIS_DB = 0
REDIS_PASSWORD = "Jeason52"
MAX_RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429, 404, 403]
RETRY_PRIORITY_ADJUST = -1

DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

# 文件及路径，log目录需要先建好
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'log')
today = datetime.now()

log_file_path = LOG_PATH + f"/scrapy_{today.year}_{today.month}_{today.day}.log"
# 日志输出
"""
1. CRITICAL - 严重错误
2. ERROR - 一般错误
3. WARNING - 警告信息
4. INFO - 一般信息
5. DEBUG - 调试信息
"""

LOG_LEVEL = "INFO"
# LOG_FILE = log_file_path
# LOG_STDOUT = True
