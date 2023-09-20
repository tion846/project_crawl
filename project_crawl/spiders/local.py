from bs4 import BeautifulSoup
from project_crawl.http import CommonSeleniumRequest
from project_crawl.items import DictionaryItem, StoreAppItem
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import gmtime, localtime, strftime, sleep
from types import SimpleNamespace
import scrapy

"""
expected_conditions
See https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html
"""


class LocalSpider(scrapy.Spider):
    name = "local"
    # allowed_domains = ["localhost"]
    start_urls = [
        "https://www.hp.com/us-en/shop/sitesearch?keyword=Laptops"
        # "http://127.0.0.1:5500/reference/index.html"
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
        fn_wait_until = EC.element_to_be_clickable((By.CLASS_NAME, "hawksearch-load-more"))

        for url in self.start_urls:
            request = CommonSeleniumRequest(url=url,
                                            callback=self.parse,
                                            wait_time=10,
                                            wait_until=fn_wait_until,
                                            script_callback=self.driver_execuate_callback)
            yield request

    def driver_execuate_callback(self, driver):
        print("[driver_execuate_callback] begin. ", strftime("%Y/%m/%d %H:%M:%S", localtime()))

        driver.find_element(By.CSS_SELECTOR,
                            "button.hawksearch-load-more").click()
        print("click", strftime("%Y/%m/%d %H:%M:%S", localtime()))
        fn_wait_until = EC.element_to_be_clickable((By.CLASS_NAME, "hawksearch-load-more"))
        WebDriverWait(driver, 10).until(fn_wait_until)

        print("[driver_execuate_callback] end. ", strftime("%Y/%m/%d %H:%M:%S", localtime()))
        # # 向下滾動
        # scroll_dowm_cmd = "window.scrollTo(0, document.body.scrollHeight);"
        # driver.execute_script(scroll_dowm_cmd)
        # # sleep(2)
        # driver.implicitly_wait(2)
        # driver.execute_script(scroll_dowm_cmd)
        # # 按按鈕
        # driver.find_element(By.CSS_SELECTOR,
        #                     "button.hawksearch-load-more").click()
        # # sleep(2)
        # driver.implicitly_wait(2)
        # driver.execute_script(scroll_dowm_cmd)
        # # sleep(2)
        # driver.implicitly_wait(2)

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
