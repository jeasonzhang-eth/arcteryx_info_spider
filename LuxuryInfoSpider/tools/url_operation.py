from itertools import product
from urllib.parse import parse_qs, urlparse, urlencode
import json


def build_url(args_dict):
    shop = args_dict.get('shop')
    gender = args_dict.get('gender')
    region = args_dict.get('region')
    start = args_dict.get('start')
    params = {
        "domain_key": f"{shop}",
        "efq": f"genders:(\"{gender}\")",
        "q": f"{gender}",
        "view_id": f"{region}",
        "start": f"{start}",
        "rows": "200",
        "request_type": "search",
        "search_type": "category",
        "account_id": "7359" if shop == 'arcteryx_outlet' else "7358",
        "fl": "gender,is_new,is_pro,is_revised,rating,review_count,"
              "slug,title,pid,description,thumb_image,price_us,price_ca,price_de",
        "url": "https://outlet.arcteryx.com/" if shop == 'arcteryx_outlet' else "https://arcteryx.com/",
        "ref_url": "https://outlet.arcteryx.com/" if shop == 'arcteryx_outlet' else "https://arcteryx.com/",
    }
    url = 'https://core.dxpapi.com/api/v1/core/?' + params_to_query(params)
    return url


def print_formatted_dict(dict_obj):
    formatted_dict = json.dumps(dict_obj, indent=4, sort_keys=True)
    print(formatted_dict)


def url_to_dict(url):
    query = urlparse(url).query
    params = parse_qs(query)
    # Extract single values from lists
    for key, value in params.items():
        if len(value) == 1:
            params[key] = value[0]
    return params


def params_to_query(params):
    return urlencode(params)


def build_all_url():
    shop_list = ['arcteryx_outlet', 'arcteryx']
    gender_list = ['men', 'women']
    region_list = ['us', 'ca', 'de']

    loop_var = [shop_list, gender_list, region_list]
    url_list = []
    args_dict_list = []
    for item in product(*loop_var):
        shop = item[0]
        gender = item[1]
        region = item[2]
        start = 0

        args_dict = {
            "shop": shop,
            "gender": gender,
            "region": region,
            "start": start
        }
        url = build_url(args_dict)
        print(url)
        url_list.append(url)
        args_dict_list.append(args_dict)
    return url_list, args_dict_list


def main():
    url = ('https://core.dxpapi.com/api/v1/core/?domain_key=arcteryx_outlet&efq=genders%3A%28%22women%22%29&q=women'
           '&view_id=ca&start=0&rows=200&request_type=search&search_type=category&account_id=7359&fl=analytics_name'
           '%2Ccollection%2Ccolour_images_map%2Ccolour_images_map_us%2Cdescription%2Cdiscount_price_us%2Cgender'
           '%2Chover_image%2Cis_new%2Cis_pro%2Cis_revised%2Cprice_us%2Cpid%2Creview_count%2Crating%2Cslug%2Ctitle'
           '%2Cthumb_image&url=https%3A%2F%2Farcteryx.com%2F&ref_url=https%3A%2F%2Farcteryx.com%2F')
    # params  = url_to_dict(url)  # 解析params
    # print_formatted_dict(params)  # 打印params
    # new_url = 'https://core.dxpapi.com/api/v1/core/?'  + params_to_query(params)
    url_list = build_all_url()


if __name__ == '__main__':
    main()


