from bs4 import BeautifulSoup
from project_crawl.share.utils import CrawlRequest, init_logging, print_line, is_env_production, get_settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from urllib.parse import urljoin, quote
import requests
import scrapy


class ShopAppSpider(scrapy.Spider):
    name = "shop_app"
    # allowed_domains = ["www.hp.com"]
    start_urls = [
        "https://www.hp.com/us-en/shop/sitesearch?keyword=Laptops"
    ]

    headers = {"User-Agent": get_settings("USER_AGENT")}
    keywords = ["Laptops", "Desktops", "Docking"]
    product_page_api_pattern = "https://www.hp.com/us-en/shop/app/api/web/graphql/page/%s/async"
    product_page_suffix = "async"

    def __init__(self, name=None, **kwargs):
        init_logging()
        super().__init__(name, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            request = CrawlRequest(url=url,
                                   callback=self.parse,
                                   before_response_callback=self.driver_before_response)
            yield request

    def driver_before_response(self, driver):
        print_line("[driver_before_response] begin.")
        driver.implicitly_wait(0)
        sleep(3)

        i = 1
        loop_flag = False
        while not loop_flag:
            if not is_env_production():
                """ 若為開發環境, 只執行部分程式碼測試功能 """
                break

            print_line(f"[loop {i}] begin.")
            btn_load_more = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "hawksearch-load-more")
                )
            )
            btn_load_more.click()
            print_line(f"[loop {i}] clicked.")

            try:
                loop_flag = WebDriverWait(driver, 2).until(
                    EC.invisibility_of_element_located(
                        (By.CLASS_NAME, "hawksearch-load-more")
                    )
                )
            except Exception:
                pass

            i += 1
            print_line(f"[loop {i}] end.")

        sleep(3)
        print_line("[driver_before_response] end.")

    def get_product_page_url(self, url):
        """ 產生Product Detail WebApi """
        product_page = url.replace("/us-en/shop/", "")
        encode_product_page = quote(product_page, safe="")
        # result = urljoin(self.product_page_api_pattern,
        #                  f"{encode_product_page}/{self.product_page_suffix}")
        result = self.product_page_api_pattern % (encode_product_page)

        return result

    def get_product_page(self, url):
        res = requests.get(url=url, headers=self.headers, timeout=5)
        result = res.json()
        data = result["data"]["page"]["pageComponents"]["pdpTechSpecs"]["technical_specifications"]

        return data

    def parse(self, response):
        dom_list = response.css(".vwaList").get()
        soup = BeautifulSoup(dom_list, features="lxml")
        cards = soup.select("div.productTile")

        print_line("total cards count: ", len(cards))

        for card in cards:
            product_name = card.find("h3").get_text()
            url = card.find("a")["href"]
            product_page_url = self.get_product_page_url(url)
            # specifications = self.get_product_page(product_page_url)

            price_inline = card.select_one(
                "div[class^=PriceBlock-module_salePriceWrapperInline]"
            )
            if price_inline:
                price_sale_wrapper = price_inline.select_one(
                    "div[class^=PriceBlock-module_salePriceWrapper]"
                )
                if price_sale_wrapper:
                    price = price_sale_wrapper.select_one("div").get_text()
                else:
                    # special case: BUNDLE AND SAVE
                    price = price_inline.select_one("div").get_text()
            else:
                price = 0

            item = {
                "name": product_name,
                "link": url,
                "sale_price": price,
                "spec_link": product_page_url,
                # "technical_specifications": specifications
            }
            yield item
