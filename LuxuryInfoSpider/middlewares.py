# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from fake_useragent import UserAgent
from scrapy.exceptions import IgnoreRequest
from scrapy.http import Request
import time


class LuxuryInfoSpiderSpiderMiddleware:
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


class RandomUserAgentMiddleware:
    def __init__(self, user_agent="Scrapy"):
        self.ua = UserAgent(min_percentage=1.3)

    def process_request(self, request, spider):
        request.headers["User-Agent"] = self.ua.random
        return None


class RandomProxyMiddleware:
    def __init__(self, proxy):
        self.proxy = proxy

    def process_request(self, request, spider):
        request.meta["proxy"] = self.proxy
        return None


class ErrorHandlingMiddleware:
    def __init__(self, crawler):
        self.logger = crawler.spider_logger
        self.max_retries = crawler.settings.getint('MAX_RETRIES', 3)
        self.retry_http_codes = set(int(x) for x in crawler.settings.getlist('RETRY_HTTP_CODES', []))
        self.priority_adjust = crawler.settings.getint('RETRY_PRIORITY_ADJUST', -1)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_response(self, request, response, spider):
        if response.status in self.retry_http_codes:
            retries = request.meta.get('retry_times', 0) + 1
            if retries <= self.max_retries:
                self.logger.debug(f"Retrying {request.url} (failed {retries} times): {response.status}")
                new_request = request.copy()
                new_request.meta['retry_times'] = retries
                new_request.dont_filter = True
                new_request.priority = request.priority + self.priority_adjust
                return new_request
            else:
                self.logger.debug(f"Gave up retrying {request.url} (failed {retries} times): {response.status}")
        return response

    def process_exception(self, request, exception, spider):
        self.logger.error(f"Error occurred when processing {request.url}: {exception}")
        retries = request.meta.get('retry_times', 0) + 1
        if retries <= self.max_retries:
            self.logger.debug(f"Retrying {request.url} (failed {retries} times): {exception}")
            new_request = request.copy()
            new_request.meta['retry_times'] = retries
            new_request.dont_filter = True
            new_request.priority = request.priority + self.priority_adjust
            return new_request


class DelayMiddleware:
    def __init__(self, delay):
        self.delay = delay

    @classmethod
    def from_crawler(cls, crawler):
        delay = crawler.settings.getfloat('DOWNLOAD_DELAY', 1.0)
        return cls(delay)

    def process_request(self, request, spider):
        time.sleep(self.delay)


class CookiesMiddleware:
    def __init__(self, cookies):
        self.cookies = cookies

    @classmethod
    def from_crawler(cls, crawler):
        cookies = crawler.settings.getdict('COOKIES', {})
        return cls(cookies)

    def process_request(self, request, spider):
        request.cookies = self.cookies


class CachingMiddleware:
    def __init__(self):
        self.cache = {}

    def process_request(self, request, spider):
        if request.url in self.cache:
            return self.cache[request.url]

    def process_response(self, request, response, spider):
        self.cache[request.url] = response
        return response
