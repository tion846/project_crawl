import scrapy
from bs4 import BeautifulSoup


class PracticeSpider(scrapy.Spider):
    name = "practice"
    # allowed_domains = ["getbootstrap.com"]
    start_urls = [
        "https://getbootstrap.com/docs/5.3/getting-started/introduction/"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        dom_nav = response.css("#bd-docs-nav").get()
        soup = BeautifulSoup(dom_nav, features="lxml")

        for section in soup.select("li.bd-links-group"):
            name = section.find("strong").get_text().strip()
            values = []

            for value in section.select("a.bd-links-link"):
                values.append(value.get_text())

            item = {
                "chapter": name,
                "count": len(values),
                "subTitle": values,
            }

            yield item
