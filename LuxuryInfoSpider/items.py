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
    shop = scrapy.Field()
    region = scrapy.Field()
    link = scrapy.Field()
    sku = scrapy.Field()

    variants_list = scrapy.Field()
    color_dict = scrapy.Field()
    size_dict = scrapy.Field()
    last_update = scrapy.Field()


class LuxuryLinkItem(scrapy.Item):
    atx_us_links = scrapy.Field(default={})
    atx_us_skus = scrapy.Field(default={})

    atx_ca_links = scrapy.Field(default={})
    atx_ca_skus = scrapy.Field(default={})

    atx_de_links = scrapy.Field(default={})
    atx_de_skus = scrapy.Field(default={})

    atxot_us_links = scrapy.Field(default={})
    atxot_us_skus = scrapy.Field(default={})

    atxot_ca_links = scrapy.Field(default={})
    atxot_ca_skus = scrapy.Field(default={})

    atxot_de_links = scrapy.Field(default={})
    atxot_de_skus = scrapy.Field(default={})


class CommoditiesItem(scrapy.Item):
    atx_us_commodities = scrapy.Field()
    atx_ca_commodities = scrapy.Field()
    atx_de_commodities = scrapy.Field()

    atxot_us_commodities = scrapy.Field()
    atxot_ca_commodities = scrapy.Field()
    atxot_de_commodities = scrapy.Field()


class CommoditiesResultItem(scrapy.Item):
    atx_us_statistics = scrapy.Field()
    atx_ca_statistics = scrapy.Field()
    atx_de_statistics = scrapy.Field()

    atxot_us_statistics = scrapy.Field()
    atxot_ca_statistics = scrapy.Field()
    atxot_de_statistics = scrapy.Field()

