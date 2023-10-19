import scrapy


class ShopDellSpider(scrapy.Spider):
    name = "shop_dell"
    # allowed_domains = ["www.dell.com"]
    start_urls = [
        "https://www.dell.com/en-us/search/laptop?p=1&t=Product",
        "https://www.dell.com/en-us/search/desktop?p=1&t=Product",
        "https://www.dell.com/en-us/search/docking?p=1&c=8407,8408&f=true&ac=categoryfacetselect",
    ]

    def parse(self, response):
        pass
