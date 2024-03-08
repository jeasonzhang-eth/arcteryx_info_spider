# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LuxuryInfoSpiderItem(scrapy.Item):
    # 以下字段是直接从网站上爬取的商品信息
    gender = scrapy.Field()
    is_new = scrapy.Field()
    is_pro = scrapy.Field()
    is_revised = scrapy.Field()
    rating = scrapy.Field()
    review_count = scrapy.Field()
    slug = scrapy.Field()
    title = scrapy.Field()
    pid = scrapy.Field()
    description = scrapy.Field()
    thumb_image = scrapy.Field()
    price_us = scrapy.Field()
    price_ca = scrapy.Field()
    price_de = scrapy.Field()

    # 以下字段是需要加工后才能产生的商品信息
    link = scrapy.Field()
    sku = scrapy.Field()
    shop = scrapy.Field()
    region = scrapy.Field()
    variants_list = scrapy.Field()
    color_dict = scrapy.Field()
    size_dict = scrapy.Field()
    last_update = scrapy.Field()