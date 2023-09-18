import json
import scrapy
from bs4 import BeautifulSoup
from project_crawl.items import DictionaryItem
from scrapy_selenium import SeleniumRequest
from types import SimpleNamespace
from scrapy.utils.project import get_project_settings

from time import gmtime, strftime
from scrapy.utils.log import configure_logging


class LocalSpider(scrapy.Spider):
    name = "local"
    # allowed_domains = ["localhost"]
    start_urls = [
        # "https://www.hp.com/us-en/shop/sitesearch?keyword=Laptops"
        # "http://127.0.0.1:5500/index.html"
        "http://localhost:5420/"
    ]

    def __init__(self, name=None, **kwargs):
        settings = get_project_settings()
        logging_folder = settings.get("LOG_FILE_FOLDER")
        log_file_name = strftime("%Y%m%d", gmtime())
        configure_logging(
            {"LOG_FILE": f"{logging_folder}\\{log_file_name}.txt"}
        )
        super().__init__(name, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            webapi_url = "http://localhost:5410/"
            js_script = f"""
                let url = "{webapi_url}PurchaseReport/QuerySetMaterialReport?classCodes=";
                let data = await fetch(url);
                let result = await data.json();
                return result;
            """
            request = SeleniumRequest(url=url,
                                      callback=self.parse,
                                      script=js_script)
            yield request

    def parse(self, response):
        js_script_result = response.css("div#js-script-result").get()
        result = BeautifulSoup(js_script_result, features="lxml").get_text()

        data_set = json.loads(result)

        for data in data_set["GridDatas"]:
            item = DictionaryItem()
            print(type(data), data)
            # item["name"] = ""
            # item["value"] = data
            # yield item

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
