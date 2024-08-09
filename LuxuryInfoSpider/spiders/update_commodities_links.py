import scrapy
import json
from redis import Redis
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.http import Response, Request
from LuxuryInfoSpider.tools.url_operation import build_all_url, build_url
from LuxuryInfoSpider.items import LuxuryLinkItem, CommoditiesItem, CommoditiesResultItem
from LuxuryInfoSpider.tools.redis_handler import RedisHandler


class UpdateCommodityLinksSpider(scrapy.Spider):
    name = "update_commodities_links"
    allowed_domains = ["core.dxpapi.com"]

    # @class method
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     settings = crawler.settings
    #     spider = cls(settings.get('REDIS_HOST'),
    #                  settings.getint('REDIS_PORT'),
    #                  settings.getint('REDIS_DB'),
    #                  settings.get('REDIS_PASSWORD'),
    #                  *args, **kwargs)
    #     spider._set_crawler(crawler)
    #     return spider

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis: Redis | None = None
        self.link_item = LuxuryLinkItem()
        self.commodity_item = CommoditiesItem()
        self.commodity_result_item = CommoditiesResultItem()
        self.commodity_dict = dict()
        for key in self.link_item.fields:
            self.link_item[key] = {}

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
        self.setup_redis()
        run_type = self.settings.get("run_type", None)
        if run_type == "all":
            url_list, args_dict_list = build_all_url()
            for url, args_dict in zip(url_list, args_dict_list):
                yield Request(url, callback=self.parse, meta={"args_dict": args_dict,
                                                              "is_first": True})
        elif run_type == "part":
            shop = self.settings.get("shop")
            region = self.settings.get("region")
            for gender in ['men', 'women']:
                args_dict = {"shop": shop, "gender": gender, "region": region, "start": 0}
                url = build_url(args_dict)
                # print(url)
                yield Request(url, callback=self.parse, meta={"args_dict": args_dict,
                                                              "first_time": False})
        else:
            self.logger.error("run_type参数错误")

    def parse(self, response: Response, **kwargs):
        # request传过来的参数
        args_dict = response.meta.get("args_dict")
        is_first = response.meta.get("is_first")

        shop = args_dict["shop"]
        if shop == "arcteryx":
            shop_key = "atx"
        else:
            shop_key = "atxot"
        region = args_dict["region"]
        # 解析json数据
        result: dict = json.loads(response.body)
        # 获取商品总数
        num_found = result.get("response").get("numFound")
        # 如果商品总数大于200，就需要发送多次请求，因为每次只能请求200个商品
        page = num_found // 200 + 1
        if page > 1 and num_found > 200 and is_first:
            for i in range(1, page):  # 从第二页开始进行获取
                args_dict["start"] = i * 200
                url = build_url(args_dict)
                yield Request(url, callback=self.parse, meta={"args_dict": args_dict,
                                                              "first_time": False})
        # 获取商品信息
        commodity_list = result.get("response").get("docs")
        # 生成商品信息Item

        commodities_key = f"{shop_key}_{region}_commodities"

        sku_list = []

        # 生成商品链接Item
        for commodity in commodity_list:
            slug = commodity.get('slug')
            pid = commodity.get('pid')
            if shop == "arcteryx_outlet" and region == 'us' and pid == 'X000005891':
                pid = 'X000007174'
            sku = pid
            sku_list.append(sku)

            link = (f"https://{'arcteryx' if shop == 'arcteryx' else 'outlet.arcteryx'}"
                    f".com/{region}/en/shop/{slug}")

            link_key = f"{shop_key}_{region}_links"
            sku_key = f"{shop_key}_{region}_skus"

            self.link_item[link_key].update({link: sku})
            self.link_item[sku_key].update({sku: link})

            self.commodity_dict.update({sku: commodity})

        self.commodity_item[commodities_key] = self.commodity_dict
        yield self.commodity_item
        yield self.link_item

        # 生成本次运行的信息Item
        commodities_statistics_key = f"{shop_key}_{region}_statistics"
        commodities_statistics_dict = {
            "total": len(commodity_list),
            "sku_list": sku_list,
        }
        self.commodity_result_item[commodities_statistics_key] = commodities_statistics_dict
        yield self.commodity_result_item


if __name__ == "__main__":
    # 获取全局配置
    setting = get_project_settings()
    # 调试参数输入
    setting.set("run_type", "all")
    setting.set("shop", "arcteryx")
    setting.set("region", "us")
    # 将设置传入爬虫进程
    process = CrawlerProcess(setting)
    # 启动爬虫
    process.crawl(UpdateCommodityLinksSpider)
    process.start()
