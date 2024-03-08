from datetime import datetime
import scrapy
from scrapy import Request
from LuxuryInfoSpider.tools.url_operation import build_all_url, build_url
import json
from LuxuryInfoSpider.items import LuxuryInfoSpiderItem


class ArcteryxSpider(scrapy.Spider):
    name = "arcteryx"
    allowed_domains = ["arcteryx.com", "core.dxpapi.com"]
    url_list, args_dict_list = build_all_url()

    def start_requests(self):
        for url, args_dict in zip(self.start_urls, self.args_dict_list):
            yield Request(url, callback=self.parse, meta={"args_dict": args_dict})

    def parse(self, response, **kwargs):
        # request传过来的参数
        args_dict = response.meta.get("args_dict")
        # 解析json数据
        result: dict = json.loads(response.body)
        # 获取商品总数
        num_found = result.get("response").get("numFound")
        # 如果商品总数大于200，就需要发送多次请求，因为每次只能请求200个商品
        page = num_found // 200 + 1
        if page > 1 and num_found > 200:
            for i in range(page):
                args_dict["start"] = i * 200
                url = build_url(args_dict)
                yield Request(url, callback=self.parse, meta={**args_dict, "start": page * 200})
        # 获取商品信息
        commodities = result.get("response").get("docs")
        for commodity in commodities:
            item = LuxuryInfoSpiderItem()
            item.update(commodity)
            item["shop"] = args_dict["shop"]
            item["region"] = args_dict["region"]
            if item["region"] == "us" and item["shop"] == "arcteryx":
                link = f"https://arcteryx.com/us/en/shop/{item['slug']}"
            elif item["region"] == "ca" and item["shop"] == "arcteryx":
                link = f"https://arcteryx.com/ca/en/shop/{item['slug']}"
            elif item["region"] == "de" and item["shop"] == "arcteryx":
                link = f"https://arcteryx.com/de/en/shop/{item['slug']}"
            elif item["region"] == "us" and item["shop"] == "arcteryx_outlet":
                link = f"https://outlet.arcteryx.com/us/en/shop/{item['slug']}"
            elif item["region"] == "ca" and item["shop"] == "arcteryx_outlet":
                link = f"https://outlet.arcteryx.com/ca/en/shop/{item['slug']}"
            elif item["region"] == "de" and item["shop"] == "arcteryx_outlet":
                link = f"https://outlet.arcteryx.com/de/en/shop/{item['slug']}"
            else:
                link = ''
            if link != '':
                item["link"] = link
                yield Request(link, callback=self.parse_detail, meta={"item": item})

    def parse_detail(self, response):
        name = self.name
        item = response.meta.get("item")
        next_data = response.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first()

        next_data = json.loads(next_data)
        product = next_data.get("props").get("pageProps").get("product")
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
