from bs4 import BeautifulSoup
from project_crawl.http import CommonSeleniumRequest
from project_crawl.items import DictionaryItem, StoreAppItem
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import gmtime, localtime, strftime, sleep
from types import SimpleNamespace
import scrapy

"""
expected_conditions
See https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html

selenium document
See https://selenium-python.readthedocs.io/index.html
"""


class LocalSpider(scrapy.Spider):
    name = "local"
    # allowed_domains = ["localhost"]
    start_urls = [
        "https://www.hp.com/us-en/shop/sitesearch?keyword=Laptops"
        # "http://127.0.0.1:5500/reference/index.html"
    ]

    def __init__(self, name=None, **kwargs):
        """ 初始化Logging檔案路徑, 取得settings.py LOG_FILE_FOLDER """
        settings = get_project_settings()
        logging_folder = settings.get("LOG_FILE_FOLDER")
        log_file_name = strftime("%Y%m%d", gmtime())
        configure_logging(
            {"LOG_FILE": f"{logging_folder}\\{log_file_name}.txt"}
        )
        super().__init__(name, **kwargs)

    def start_requests(self):
        # fn_wait_until = EC.element_to_be_clickable((By.CLASS_NAME, "hawksearch-load-more"))

        for url in self.start_urls:
            request = CommonSeleniumRequest(url=url,
                                            callback=self.parse,
                                            # wait_time=10,
                                            # wait_until=fn_wait_until,
                                            script_callback=self.driver_execuate_callback)
            yield request

    def driver_execuate_callback(self, driver):
        self.print_message("[driver_execuate_callback] begin.")
        driver.implicitly_wait(0)
        sleep(3)

        # TODO:
        i = 1;
        loop_flag = False
        while not loop_flag:
            self.print_message(f"[loop {i}] begin.")
            btn_load_more = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "hawksearch-load-more"))
            )
            btn_load_more.click()
            self.print_message(f"[loop {i}] clicked.")

            try:
                loop_flag = WebDriverWait(driver, 2).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "hawksearch-load-more"))
                )
            except Exception:
                pass

            i += 1
            self.print_message(f"[loop {i}] end.")

            if i >= 20:
                self.print_message(f"[loop {i}] break.")
                break

        # fn_wait_until_visibility = EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.vwaList div.productTile"))
        # WebDriverWait(driver, 10).until(fn_wait_until_visibility)

        self.print_message("[driver_execuate_callback] end.")
        sleep(3)

    def parse(self, response):
        dom_list = response.css(".vwaList").get()
        soup = BeautifulSoup(dom_list, features="lxml")
        cards = soup.select("div.productTile")

        self.print_message(f"total cards count: {len(cards)}")

        for card in cards:
            product_name = card.find("h3").get_text()
            url = card.find("a")["href"]

            # TODO:
            price_inline = card.select_one("div[class^=PriceBlock-module_salePriceWrapperInline]")
            if price_inline:
                price_sale_wrapper = price_inline.select_one("div[class^=PriceBlock-module_salePriceWrapper]")
                if price_sale_wrapper:
                    price = price_sale_wrapper.select_one("div").get_text()
                else:
                    # BUNDLE AND SAVE
                    price = price_inline.select_one("div").get_text()
            else:
                price = 0

            item = StoreAppItem()
            item["product_name"] = product_name
            item["url"] = url
            item["price"] = price
            yield item

    def print_message(self, message):
        current = strftime("%Y-%m-%d %H:%M:%S", localtime())
        print(f"[{current}] {message}")