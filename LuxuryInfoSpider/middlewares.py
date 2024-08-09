# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.exceptions import IgnoreRequest
from scrapy.http import Request, Response
from scrapy.spiders.crawl import Spider
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from random_useragent import UserAgent
import time
import requests
from random import randint


api_key = '04360a45-1248-4099-ba58-5f77272a109b'


def get_headers_list():
    params = {
        'api_key': '04360a45-1248-4099-ba58-5f77272a109b',
        'num_results': '100'}
    response = requests.get(url='http://headers.scrapeops.io/v1/browser-headers?api_key=' + api_key, params=params)
    json_response = response.json()
    return json_response.get('result', [])


def get_random_header(header_list):
    random_index = randint(0, len(header_list) - 1)
    return header_list[random_index]


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

    def process_spider_input(self, response: Response, spider: Spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response: Response, result, spider: Spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response: Response, exception, spider: Spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider: Spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider: Spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class RandomUserAgentMiddleware:
    def __init__(self):
        self.ua = UserAgent()
        self.logger = logging.getLogger(__name__ + ".RandomUserAgentMiddleware")

    def process_request(self, request: Request, spider: Spider):
        # user_agent = self.ua.generate_mac_chrome_ua()
        # print(user_agent)

        # headers = {
        #     'authority': 'arcteryx.com',
        #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        #     'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        #     'cache-control': 'max-age=0',
        #     'if-none-match': 'W/"1ee97-KgcCYjUXtJN8mSMgHMMkyEXdIb4"',
        #     'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        #     'sec-ch-ua-mobile': '?0',
        #     'sec-ch-ua-platform': '"macOS"',
        #     'sec-fetch-dest': 'document',
        #     'sec-fetch-mode': 'navigate',
        #     'sec-fetch-site': 'none',
        #     'sec-fetch-user': '?1',
        #     'upgrade-insecure-requests': '1',
        #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        # }
        # playwright_context_kwargs = request.meta.get("playwright_context_kwargs", {})
        # playwright_context_kwargs["extra_http_headers"] = headers
        # request.meta["playwright_context_kwargs"] = playwright_context_kwargs
        header_list = get_headers_list()
        request.headers.update(get_random_header(header_list))
        # request.headers["User-Agent"] = self.ua.random
        return None

    # async def process_response(self, request, response, spider):
    #     if request.meta.get("playwright", False) is False:
    #         return response  # 仅处理 Playwright 请求
    #
    #     page = response.meta["playwright_page"]
    #     headers = await page.evaluate(
    #         "() => { return window.performance.getEntriesByType('resource')[0].requestHeaders }")
    #     self.logger.info(f"Request Headers for {request.url}:")
    #     for key, value in headers.items():
    #         self.logger.info(f"  {key}: {value}")
    #
    #     return response


# noinspection PyMethodMayBeStatic
class RandomProxyMiddleware:
    def __init__(self, crawler: Crawler):
        self.max_retry_times = crawler.settings.getint('MAX_RETRY_TIMES', 3)
        self.logger = logging.getLogger(__name__ + ".RandomProxyMiddleware")
        pass

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        return cls(crawler)

    @classmethod
    def get_proxy(cls, logger):
        response = requests.get("http://localhost:5010/get/")
        status_code = response.status_code
        if status_code == 200:
            proxy_str = json.loads(response.text).get("proxy")
            if proxy_str:
                proxy = f"http://{proxy_str}"
                logger.info(f"Using proxy: {proxy}")
                return proxy_str
            else:
                logger.info(f"No proxy available now")
                return None

    @classmethod
    def delete_proxy(cls, proxy: str, logger):
        while True:
            proxy_str = proxy.split("//")[1]
            response = requests.get(f"http://localhost:5010/delete/?proxy={proxy_str}")
            status_code = response.status_code
            if status_code == 200:
                logger.info(f"Deleted proxy: {proxy_str}")
                return True
            else:
                logger.info(f"Delete Failed")
                return False

    def process_request(self, request, spider: Spider):
        is_parse_detail = request.meta.get("is_parse_detail")
        if is_parse_detail:
            proxy_str = self.get_proxy(self.logger)
            proxy = f"http://{proxy_str}"
            if proxy:
                # playwright_context_kwargs = request.meta.get("playwright_context_kwargs", {})
                # playwright_context_kwargs["proxy"] = {
                #     "server": proxy,
                #     "username": "",
                #     "password": ""
                # }
                # request.meta["playwright_context_kwargs"] = playwright_context_kwargs
                # self.logger.info(playwright_context_kwargs)

                request.meta["proxy"] = proxy
                self.logger.info(request.meta["proxy"])
            # print(request.meta)
            return None


class ErrorHandlingMiddleware:
    def __init__(self, crawler: Crawler):
        self.logger = logging.getLogger(__name__ + ".ErrorHandlingMiddleware")
        self.max_retry_times = crawler.settings.getint('MAX_RETRY_TIMES')
        self.retry_http_codes = set(int(x) for x in crawler.settings.getlist('RETRY_HTTP_CODES'))
        self.priority_adjust = crawler.settings.getint('RETRY_PRIORITY_ADJUST')

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        return cls(crawler)

    def process_response(self, request: Request, response: Response, spider: Spider):
        if response.status in self.retry_http_codes:
            return self._retry(request, response.status, spider)
        return response

    def process_exception(self, request, exception, spider):
        self.logger.error(f"Error occurred when processing {request.url}: {exception}")
        return self._retry(request, exception, spider)

    def _retry(self, request: Request, reason, spider: Spider):
        retries = request.meta.get('retry_times', 0) + 1
        if retries <= self.max_retry_times:
            self.logger.info(f"Retrying {request.url} (failed {retries} times): {reason}")
            old_proxy = request.meta["proxy"]
            RandomProxyMiddleware.delete_proxy(old_proxy, self.logger)
            new_request = request.copy()
            # proxy = RandomProxyMiddleware.get_proxy(self.logger)
            # new_request.meta["proxy"] = proxy
            new_request.meta['retry_times'] = retries
            new_request.dont_filter = True
            new_request.priority = request.priority + self.priority_adjust
            return new_request
        else:
            self.logger.info(f"Gave up retrying {request.url} (failed {retries} times): {reason}")
            raise IgnoreRequest(f"Gave up retrying {request.url} (failed {retries} times)")


class DelayMiddleware:
    def __init__(self, crawler):
        self.delay = crawler.settings.getfloat('DOWNLOAD_DELAY', 1.0)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        is_parse_detail = request.meta.get("is_parse_detail")
        if is_parse_detail:
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
