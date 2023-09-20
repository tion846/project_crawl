from bs4 import BeautifulSoup
from project_crawl.http import CommonSeleniumRequest
from project_crawl.items import DictionaryItem, StoreAppItem
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from time import gmtime, strftime, sleep
from types import SimpleNamespace
import scrapy


class LocalSpider(scrapy.Spider):
    name = "local"
    # allowed_domains = ["localhost"]
    start_urls = [
        # "https://www.hp.com/us-en/shop/sitesearch?keyword=Laptops"
        "http://127.0.0.1:5500/reference/index.html"
    ]

    def __init__(self, name=None, **kwargs):
        """ 初始化Logging檔案路徑, 取得settings.py LOG_FILE_FOLDER"""
        settings = get_project_settings()
        logging_folder = settings.get("LOG_FILE_FOLDER")
        log_file_name = strftime("%Y%m%d", gmtime())
        configure_logging(
            {"LOG_FILE": f"{logging_folder}\\{log_file_name}.txt"}
        )
        super().__init__(name, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            request = CommonSeleniumRequest(url=url,
                                            callback=self.parse,
                                            script_callback=self.driver_execuate_callback)
            yield request

    def driver_execuate_callback(self, driver):
        # 向下滾動
        scroll_dowm_cmd = "window.scrollTo(0, document.body.scrollHeight);"
        driver.execute_script(scroll_dowm_cmd)
        sleep(2)
        driver.execute_script(scroll_dowm_cmd)
        # 按按鈕
        button = driver.find_elements(By.CSS_SELECTOR,
                                      'button.hawksearch-load-more')
        button[0].click()
        sleep(2)
        driver.execute_script(scroll_dowm_cmd)
        sleep(2)

    def parse(self, response):
        dom_list = response.css(".vwaList").get()
        soup = BeautifulSoup(dom_list, features="lxml")
        cards = soup.select("div.productTile")

        for card in cards:
            product_name = card.find("h3").get_text()
            url = card.find("a")["href"]
            price = card.select_one(
                "div[class^=PriceBlock-module_salePriceWrapper] div").get_text()

            item = StoreAppItem()
            item["product_name"] = product_name
            item["url"] = url
            item["price"] = price
            yield item
