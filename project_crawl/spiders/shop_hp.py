from bs4 import BeautifulSoup
from project_crawl.share.utils import CrawlRequest, init_logging, print_line, is_env_production, get_settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from urllib.parse import quote, urlparse, parse_qs

import scrapy


class ShopHpSpider(scrapy.Spider):
    name = "shop_hp"
    allowed_domains = ["www.hp.com"]
    # start_urls = [
    #     # "https://www.hp.com/us-en/shop/sitesearch?keyword=Laptops",
    #     # "https://www.hp.com/us-en/shop/sitesearch?keyword=Desktops",
    #     # "https://www.hp.com/us-en/shop/sitesearch?keyword=Docking",
    # ]

    start_urls = "https://www.hp.com/us-en/shop/sitesearch?keyword=%s"
    custom_settings = {
        # ["DEVELOPMENT", "PRODUCTION"]
        "ENVIRONMENT": "DEVELOPMENT",
        "ITEM_PIPELINES": {
            "project_crawl.pipelines.JsonWriterPipeline": 300,
            "project_crawl.pipelines.SQLWriterPipeline": 310,
        }
    }

    # headers = {"User-Agent": get_settings("USER_AGENT")}
    keywords = [
        "Laptops",
        "Desktops",
        "Docking"
    ]
    product_webapi_pattern = "https://www.hp.com/us-en/shop/app/api/web/graphql/page/%s/async"

    def __init__(self, name=None, **kwargs):
        init_logging()
        super(ShopHpSpider, self).__init__(name, **kwargs)

    def start_requests(self):
        for keyword in self.keywords:
            url = self.start_urls % (keyword)
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
            print_line(f"[loop {i}] begin.")

            try:
                btn_load_more = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.CLASS_NAME, "hawksearch-load-more")
                    )
                )
                btn_load_more.click()
                print_line(f"[loop {i}] clicked.")
            except Exception:
                print_line(f"[loop {i}] terminated.")
                break

            if not is_env_production():
                """ 若為開發環境, 只執行部分程式碼測試功能 """
                break

            try:
                loop_flag = WebDriverWait(driver, 5).until(
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

    def get_product_detail_webapi(self, url):
        """ 產生Product Detail WebApi """
        product_page = url.replace("/us-en/shop/", "")
        encode_product_page = quote(product_page, safe="")
        result = self.product_webapi_pattern % (encode_product_page)

        return result

    def parse(self, response):
        parsed_url = urlparse(response.url)
        query_string = parse_qs(parsed_url.query)
        category = query_string["keyword"][0]

        dom_list = response.css(".vwaList").get()
        soup = BeautifulSoup(dom_list, features="lxml")
        cards = soup.select("div.productTile")

        print_line("total cards count: ", len(cards))

        for card in cards:
            product_name = card.find("h3").get_text()
            url = card.find("a")["href"]
            product_detail_webapi = self.get_product_detail_webapi(url)

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
                # "Type": "",
                "Brand": "HP",
                "Category": category,
                "Name": product_name,
                "Link": url,
                "Sale_Price": price,
                "Spec_Api": product_detail_webapi,
            }
            yield item
