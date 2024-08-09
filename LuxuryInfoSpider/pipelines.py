import json
from LuxuryInfoSpider.items import LuxuryInfoSpiderItem, LuxuryLinkItem, CommoditiesItem, CommoditiesResultItem
from LuxuryInfoSpider.tools.redis_handler import RedisHandler


class RedisPipeline:
    name = ''

    def __init__(self):
        self.redis: RedisHandler | None = None
        self.link_item = None
        self.commodity_item = None
        self.commodities_result_item = None

    @classmethod
    def from_crawler(cls, crawler):
        cls.redis_host = crawler.settings.get('REDIS_HOST')
        cls.redis_port = crawler.settings.get('REDIS_PORT')
        cls.redis_db = crawler.settings.get('REDIS_DB')
        cls.redis_password = crawler.settings.get('REDIS_PASSWORD')
        return cls()

    def open_spider(self, spider):
        self.redis = RedisHandler(host=self.redis_host,
                                  port=self.redis_port,
                                  db=self.redis_db,
                                  max_connections=5,
                                  password=self.redis_password)

    def process_item(self, item, spider):
        if isinstance(item, LuxuryInfoSpiderItem):
            item = self.process_info_item(item, spider)
        if isinstance(item, LuxuryLinkItem):
            item = self.process_link_item(item, spider)
        if isinstance(item, CommoditiesItem):
            item = self.process_commodity_item(item, spider)
        if isinstance(item, CommoditiesResultItem):
            item = self.process_commodity_result_item(item, spider)
        return item

    def process_info_item(self, item, spider):
        # 将item设置到redis中
        sku = item['sku']
        shop = item['shop']
        region = item['region']
        redis_key = f"{shop}:{region}:{sku}"
        for key, value in item.items():
            self.redis.set_hash_value(redis_key, key, value)
        print(f"设置完成,商品{shop}:{region}:{sku}已经存入redis中")
        return item

    def process_link_item(self, item, spider):
        self.link_item = item
        return {}

    def process_commodity_item(self, item, spider):
        self.commodity_item = item
        return {}

    def process_commodity_result_item(self, item, spider):
        self.commodities_result_item = item
        return {}

    def close_spider(self, spider):
        link_total = 0
        sku_total = 0

        if self.commodity_item:
            for commodities_key, commodities_list in self.commodity_item.items():
                shop, region, _ = commodities_key.split("_")

                # redis命名规范是使用:分割的,所以这里需要重新拼接
                commodities_new_key = f"{shop}:{region}:commodities"

                self.redis.set_hash_value("commodities", commodities_new_key,
                                          json.dumps(commodities_list))

        if self.commodities_result_item:

            # 和这一次的结果进行比较
            for commodities_result_key, commodities_result_dict in self.commodities_result_item.items():
                shop, region, _ = commodities_result_key.split("_")
                commodity_statistics_key = f"{shop}:{region}:statistics"
                self.redis.set_hash_value("commodities_statistics", commodity_statistics_key,
                                          json.dumps(commodities_result_dict))

        if self.link_item:
            for key, dicts in self.link_item.items():
                shop, region, key_type = key.split("_")
                # redis命名规范是使用:分割的,所以这里需要重新拼接
                new_key = f"{shop}:{region}:{key_type}"
                if key_type == "links":
                    link_total += len(dicts)
                if key_type == "skus":
                    sku_total += len(dicts)
                for sub_key, value in dicts.items():
                    self.redis.set_hash_value(new_key, sub_key, value)

        print(f"redis连接关闭,共有link{link_total}个,共有sku{sku_total}个")
        self.redis.close()
