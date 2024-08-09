import unittest
from LuxuryInfoSpider.middlewares import RandomProxyMiddleware
from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner


class ProxyTestCase(unittest.TestCase):
    def test_get_proxy(self):
        import requests
        proxy_res = RandomProxyMiddleware().get_proxy()
        print(proxy_res)
        proxy = {
            "http": f"{proxy_res}",
            "https": f"{proxy_res}"
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Host': 'arcteryx.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Sec-Fetch-Dest': 'document',
            'Connection': 'keep-alive',
            'Cookie': 'bounceClientVisit4467=N4IgJglmIFwgbAFgOzIKyIAypQTnQIzxqYgA0IAblLAcpmgMxoGOZ0Ac88qFlsoAKaVBAJwD6AGwD2Ac1mCw4iADtYAMwCGkgM6CKOgK4AjALYQALhcXjpKnZcEbteihAAOYgMaD3FiHawIFq6TgC+FOqUFrTwuLiYAExx8IwUmtKwmBSS7kEAFlbuOgCkjACCJYkAYlXVmqJe1qIAngAeAHRe0qZ1hqU1gip1OvnS7nUiKhaaALSyMiLkIJo6WXzu-DAEFNBw0BSiQcte0bT0TCxsOyAOe2gUsl5HMMjwFKbrIJJn2xfMrEwiAoXk0pncmggsnsAhABEQ8PgrFhPxifwYALYwO+mmoezoGKu7GQXB4yBymnOhMBN3UOkp2ziCWSuFS6TWMDSK0yMA4FGkDIA2gBdPhbG642gRECJNjEXCIFG-AlMAgMNUUvG0ClU1Xq7LBelUxC4RhcLDpHmJflC0UgADuXmNpvNXNWUrCYSAA; _px2=eyJ1IjoiMTJkMDYxMDAtYjNkYi0xMWVlLTkxM2UtOWJlMTdlYjgzNGEwIiwidiI6IjY4MWMzNDcxLTdhNjEtMTFlZS04NzViLWYxNTk3YjQ0YzBiOCIsInQiOjE3MDUzODgxNzM0MjksImgiOiJjNWU4YzcxZGRiNzU2MTc5OGRlYmNkODNjNmZiMDA3ZWY4NTZmZGQ2Yzc2NjI0ZTVmODdkMThhNzViN2UxMmNjIn0; ipe.32236.pageViewedCount=2; ipe.32236.pageViewedDay=16; ipe_32236_fov=%7B%22numberOfVisits%22%3A5%2C%22sessionId%22%3A%224681558f-e88b-e5d6-5c6e-eb98f4e7f033%22%2C%22expiry%22%3A%222024-02-02T14%3A10%3A57.746Z%22%2C%22lastVisit%22%3A%222024-01-15T20%3A41%3A59.716Z%22%7D; country=us; language=en; _evga_a7e2={%22uuid%22:%22b9c84081621a383b%22}; _fbp=fb.1.1704291045580.1573018573; _gcl_au=1.1.1692033014.1704291047; s_ecid=MCMID%7C67080891722726307511937472372596145475; _pxhd=2f57ba283113f512c3a3cd2d7cca396b7b79971fb6812a1d8332c3e93f33c287:681c3471-7a61-11ee-875b-f1597b44c0b8; _screload=; enableClickAndCollectCA=true; enableClickAndCollectUS=true; enableEnhancedAssets=true; enableMixedOrders=true; enableOutletFlashSaleModal=false; enableSerratusFeatures=true; _br_uid_2=uid%3D9444916934330%3Av%3D15.0%3Ats%3D1704291047689%3Ahc%3D37; _ga_84KZ7F7FWP=GS1.1.1705351300.10.0.1705351301.59.0.0; _ga_N8XJLJFM2Z=GS1.1.1705351299.3.1.1705351301.58.0.0; _pin_unauth=dWlkPVltUTFNalZqWVRjdFpUa3lPQzAwTlRFNExUbG1OVEF0TWpBeVpESXhaVFJqTVRZNA; _scid_r=8121de91-f4a2-4694-920b-49fa5a9c48a9; _sfid_836c={%22anonymousId%22:%22b9c84081621a383b%22%2C%22consents%22:[]}; _uetsid=80d1ee60b38711ee8277bf8e6a4d27d6; _uetvid=776e04d07a6111eeb919037a74749de7; s_cc=true; prevPageType=product-page; _ga=GA1.2.745295316.1704291046; _gid=GA1.2.1296227053.1705310504; facebookConversionGuid={%22viewContentGuid%22:%22fb14431b-e840-c90f-e69a-20a605ac01b3%22%2C%22pageViewGuid%22:%2269f16cac-7184-800a-4c2b-8fa3ddb9c300%22%2C%22addToCartGuid%22:%22ae7cbe9c-4efd-7381-89cb-712dfc26092f%22}; _hjSessionUser_33114=eyJpZCI6IjVlNjRmN2I2LTI5YTktNTFjNi05YzU5LTllMGM0N2E4MGJiMiIsImNyZWF0ZWQiOjE3MDQyOTEwNDQ5OTksImV4aXN0aW5nIjp0cnVlfQ; OptanonConsent=isGpcEnabled; incap_ses_170_796389=Lc5/QFH/bi+OqUW3PvZbAoCYpWUAAAAAfEmNWXq7/oJX6GT4VVgN1Q; nlbi_796389=egb6X01dKzTw4Qp3hIcMbwAAAAAEyYObN+/cVnMu7gpLwM0I; enableBrochureMode=false; AMCV_DFBF2C1653DA80920A490D4B%40AdobeOrg=179643557%7CMCMID%7C67080891722726307511937472372596145475%7CMCIDTS%7C19738%7CMCAID%7CNONE%7CMCOPTOUT-1705353600s%7CNONE%7CMCAAMLH-1705951200%7C11%7CMCAAMB-1705951200%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCSYNCSOP%7C411-19745%7CvVersion%7C5.5.0; _ALGOLIA=anonymous-98412516-e317-4772-9050-3df7b7d07c01; incap_ses_1308_796389=4a7lDHZW3lZ9sIy6AfQmElaFpWUAAAAAmsxuyLsM/6RFRBxku1lsbA; ipe_s=4681558f-e88b-e5d6-5c6e-eb98f4e7f033; pxcts=7f28f497-b387-11ee-9d3a-85adb66fb274; AMCVS_DFBF2C1653DA80920A490D4B%40AdobeOrg=1; incap_ses_173_796389=QOH5MX6JDC6P5mbww55mAiP5pGUAAAAALOwlZ3kFz4iX+C7rDxpedg; enableFredhopperLive1Env=(null); enableFredhopperTest1Env=(null); __olapicU=1704942428080; _sctr=1%7C1704906000000; BVBRANDID=0c9ec192-4111-487c-943c-31aa741a29d3; _tt_enable_cookie=1; _ttp=tt9ufGuVPDu-lWf4vWTNJYFRpQk; _scid=8121de91-f4a2-4694-920b-49fa5a9c48a9; OptanonAlertBoxClosed=2024-01-03T14:10:44.775Z; _pxvid=681c3471-7a61-11ee-875b-f1597b44c0b8; visid_incap_796389=jqWAcvZ1Q8OP+62VBT5uS55qlWUAAAAAQUIPAAAAAABGuA+XVbS9xJMblCXbXlX2'
        }

        response = requests.get("https://arcteryx.com/us/en/shop/venta-glove", proxies=proxy, headers=headers, timeout=10, verify=False)

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    if is_running_under_teamcity():
        runner = TeamcityTestRunxner()
    else:
        runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)

