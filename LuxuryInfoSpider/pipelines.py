from LuxuryInfoSpider.items import LuxuryInfoSpiderItem

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import redis


class RedisPipeline:
    name = ''

    def __init__(self):
        self.redis = None

    @classmethod
    def from_crawler(cls, crawler):
        cls.redis_host = crawler.settings.get('REDIS_HOST')
        cls.redis_port = crawler.settings.get('REDIS_PORT')
        cls.redis_db = crawler.settings.get('REDIS_DB')
        return cls()

    def open_spider(self, spider):
        self.redis = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db)

    def process_item(self, item, spider):
        # 将item设置到redis中
        self.redis.hset()
        return item

    def close_spider(self, spider):
        self.redis.close()
