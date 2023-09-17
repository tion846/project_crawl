import scrapy
from bs4 import BeautifulSoup
from project_crawl.items import DictionaryItem


class LocalSpider(scrapy.Spider):
    name = "local"
    # allowed_domains = ["localhost"]
    start_urls = [
        # "https://www.hp.com/us-en/shop/vwa/laptops/segm=Business,Home"
        "http://127.0.0.1:5500/index.html"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.css("title")
        print(title)

        dom_list = response.css(".vwaList").get()
        soup = BeautifulSoup(dom_list, features="lxml")

        cards = soup.select("div.productTile")
        for index, card in enumerate(cards):
            name = card.find("h3").get_text()
            value = card.find("a")["href"]

            item = DictionaryItem()
            item["index"] = index
            item["name"] = name
            item["value"] = value
            yield item
