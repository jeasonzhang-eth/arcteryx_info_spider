from datetime import datetime
import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response
from scrapy.utils.project import get_project_settings
from scrapy_playwright.page import PageMethod

from LuxuryInfoSpider.tools.redis_handler import RedisHandler
import json
from LuxuryInfoSpider.items import LuxuryInfoSpiderItem
from urllib.parse import urlencode, quote


def get_scrapeops_url(url, api_key):
    payload = {
        'api_key': api_key,
        'url': url,
        'render_js': 'false',
        'residential': 'false',
        'country': 'us',
    }
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class CrawlSkusSpider(scrapy.Spider):
    name = "crawl_skus"
    allowed_domains = ["arcteryx.com"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis: RedisHandler | None = None

    def __del__(self):
        # 关闭Redis连接
        if hasattr(self, 'redis_conn') and self.redis:
            self.redis.close()

    def setup_redis(self):
        host = self.settings.get('REDIS_HOST')
        port = self.settings.getint('REDIS_PORT')
        db = self.settings.getint('REDIS_DB')
        password = self.settings.get('REDIS_PASSWORD')
        self.redis = RedisHandler(host, port, db, 5, password)

    def start_requests(self):
        api_key = '04360a45-1248-4099-ba58-5f77272a109b'

        self.setup_redis()
        self.logger.info("start_requests")
        commodity_dict_list_str_str = self.settings.get("all_commodity_dict_list_str")
        # 获取监控sku列表
        commodity_dict_list = json.loads(commodity_dict_list_str_str)
        for commodity_dict in commodity_dict_list:
            shop = commodity_dict.get("shop")
            if shop == "arcteryx":
                shop_key = "atx"
            else:
                shop_key = "atxot"
            region = commodity_dict.get("region")
            sku = commodity_dict.get("sku")
            # 获取sku链接
            link_key = f"{shop_key}:{region}:skus"
            link_dict = self.redis.hgetall(link_key)
            # 获取商品信息
            commodities_shop_region_dict = self.redis.hgetall("commodities")
            commodities_shop_region_key = f"{shop_key}:{region}:commodities"
            commodities_sku_dict = json.loads(commodities_shop_region_dict[commodities_shop_region_key])
            link = link_dict[sku]
            api_url = get_scrapeops_url(link, api_key)

            yield Request(api_url, callback=self.parse, meta={
                # "playwright": True,
                # "playwright_include_page": True,
                # "errback": self.errback,
                # "playwright_page_methods": [
                #     PageMethod("evaluate",
                #                "() => { console.log(JSON.stringify(window.performance.getEntriesByType('resource')["
                #                "0].requestHeaders)) }")
                # ],
                "shop": shop,
                "region": region,
                "sku": sku,
                "commodities_sku_dict": commodities_sku_dict,
                "is_parse_detail": True,
                'download_timeout': 30})
            self.logger.info("Start request: %s" % link)

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
        await page.context.close()

    async def parse(self, response: Response, **kwargs):
        # page = response.meta["playwright_page"]
        # headers = await page.evaluate(
        #     "() => { return window.performance.getEntriesByType('resource')[0].requestHeaders }")
        # print(headers)
        shop = response.meta["shop"]
        region = response.meta["region"]
        commodities_sku_dict = response.meta["commodities_sku_dict"]
        sku = response.meta["sku"]

        commodity = commodities_sku_dict[sku]
        item = LuxuryInfoSpiderItem()
        item['shop'] = shop
        item['region'] = region

        item["gender"] = commodity.get('gender')
        item["is_new"] = commodity.get('is_new')
        item["is_pro"] = commodity.get('is_pro')
        item["is_revised"] = commodity.get('is_revised')
        item["rating"] = commodity.get('rating') if commodity.get('rating') else ""
        item["review_count"] = commodity.get('review_count') if commodity.get('review_count') else ""
        item["slug"] = slug = commodity.get('slug')
        item["title"] = commodity.get('title')

        pid = commodity.get('pid')
        if shop == "arcteryx_outlet" and region == 'us' and pid == 'X000005891':
            pid = 'X000007174'
        item["pid"] = pid
        item["description"] = commodity.get('description')
        item["thumb_image"] = commodity.get('thumb_image')
        item["price_us"] = commodity.get('price_us')
        item["price_ca"] = commodity.get('price_ca')
        item["price_de"] = commodity.get('price_de')
        item["link"] = link = (f"https://{'arcteryx' if shop == 'arcteryx' else 'outlet.arcteryx'}"
                               f".com/{region}/en/shop/{slug}")
        item["sku"] = sku = pid
        next_data = response.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first()
        next_data = json.loads(next_data)
        product_str = next_data.get("props").get("pageProps").get("product")
        product = json.loads(product_str)
        if isinstance(product, dict):
            sku = product['id']
            color_options = product['colourOptions']
            size_options = product['sizeOptions']
            variants = product['variants']

            color_dict = {}
            for color in color_options['options']:
                label = color['label']
                value = color['value']
                color_dict[value] = label

            size_dict = {}
            for size in size_options['options']:
                label = size['label']
                value = size['value']
                size_dict[value] = label

            variants_list = []
            for variant in variants:
                color_id = variant['colourId']
                size_id = variant['sizeId']
                temp = {
                    "variant_sku": variant['id'],
                    "upc": variant['upc'],
                    "color_id": variant['colourId'],
                    "size_id": variant['sizeId'],
                    "color": color_dict[color_id],
                    "size": size_dict[size_id],
                    "inventory": variant['inventory'],
                    "price": variant['price'],
                    "discount_price": variant['discountPrice']
                }
                variants_list.append(temp)

            item['sku'] = sku
            item['size_dict'] = json.dumps(size_dict)
            item['color_dict'] = json.dumps(color_dict)
            item['variants_list'] = json.dumps(variants_list)
            item['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield item
        else:
            print(product)
        # await page.close()
        # await page.context.close()


if __name__ == "__main__":
    # 获取全局配置
    setting = get_project_settings()
    setting.set("all_commodity_dict_list_str", '['
                                               # '{"shop": "arcteryx", "region": "ca", "sku": "X000009309"}, '
                                               # '{"shop": "arcteryx", "region": "de", "sku": "X000007397"}, '
                                               # '{"shop": "arcteryx", "region": "us", "sku": "X000006826"}, '
                                               # '{"shop": "arcteryx", "region": "us", "sku": "X000006773"}, '
                                               # '{"shop": "arcteryx_outlet", "region": "ca", "sku": "X000007510"}, '
                                               # '{"shop": "arcteryx_outlet", "region": "de", "sku": "X000006381"}, '
                                               '{"shop": "arcteryx_outlet", "region": "us", "sku": "X000007194"}]')
    # 调试参数输入

    """

    [
    {"shop": "arcteryx", "region": "ca", "sku": "X000009309"}, 
    {"shop": "arcteryx", "region": "de", "sku": "X000007397"}, 
    {"shop": "arcteryx", "region": "us", "sku": "X000006826"}, 
    {"shop": "arcteryx", "region": "us", "sku": "X000006773"}, 
    {"shop": "arcteryx_outlet", "region": "ca", "sku": "X000007510"}, 
    {"shop": "arcteryx_outlet", "region": "de", "sku": "X000006381"}, 
    {"shop": "arcteryx_outlet", "region": "us", "sku": "X000007194"}]

    """
    # 将设置传入爬虫进程
    process = CrawlerProcess(setting)
    # 启动爬虫
    process.crawl(CrawlSkusSpider)
    process.start()
