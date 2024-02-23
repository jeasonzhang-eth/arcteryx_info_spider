import scrapy


class ArcteryxSpider(scrapy.Spider):
    name = "arcteryx"
    allowed_domains = ["arcteryx.com"]
    start_urls = ["https://arcteryx.com/"]

    def parse(self, response):
        pass
