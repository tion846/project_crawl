from project_crawl.share.utils import CrawlRequest, init_logging, print_line, is_env_production, get_settings
import scrapy

import requests


class ShopHpDetailSpider(scrapy.Spider):
    name = "shop_hp_detail"
    allowed_domains = ["www.hp.com"]
    start_urls = ["https://www.hp.com"]

    def parse(self, response):
        pass

    def get_product_detail(self, url):
        res = requests.get(url=url, headers=self.headers, timeout=5)
        result = res.json()
        data = result["data"]["page"]["pageComponents"]["pdpTechSpecs"]["technical_specifications"]

        return data
