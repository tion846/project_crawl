from project_crawl.share.models import Product
from project_crawl.share.utils import init_logging, print_line, get_settings, get_db_connect_string
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

import scrapy


class ShopHpDetailSpider(scrapy.Spider):
    name = "shop_hp_detail"
    # allowed_domains = ["www.hp.com"]
    start_urls = [
        "https://www.hp.com/us-en/shop/app/api/web/graphql/page/pdp%2Fhp-envy-x360-2-in-1-laptop-15t-fe000-156-77x87av-1/async",
        # "https://www.hp.com/us-en/shop/app/api/web/graphql/page/pdp%2Fomen-gaming-laptop-16t-wf000-161-76w27av-1/async"
    ]
    products = []

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        # ["DEVELOPMENT", "PRODUCTION"]
        "ENVIRONMENT": "DEVELOPMENT",
        "DOWNLOADER_MIDDLEWARES": {
            "project_crawl.middlewares.SeleniumMiddleware": None,
            # "project_crawl.middlewares.HttpRequestMiddleware": 540,
        },
        # "ITEM_PIPELINES": {
        #     "project_crawl.pipelines.JsonWriterPipeline": 300,
        #     "project_crawl.pipelines.SQLWriterPipeline": 310,
        # },
    }

    headers = {"User-Agent": get_settings("USER_AGENT")}

    def __init__(self, name=None, **kwargs):
        init_logging()
        db_connect_string = get_db_connect_string()
        engine = create_engine(f"sqlite:///{db_connect_string}", echo=True)

        with Session(engine) as session:
            self.products = session.scalars(select(Product).limit(5)).all()

        super(ShopHpDetailSpider, self).__init__(name, **kwargs)

    def start_requests(self):
        for item in self.products:
            yield scrapy.Request(
                url=item.Spec_Api,
                method='GET',
                headers=self.headers,
                callback=self.parse,
                cb_kwargs={"item": item}
            )

    def parse(self, response, item):
        print_line(item)
        print_line(response)
        pass

    # def get_product_detail(self, url):
    #     res = requests.get(url=url, headers=self.headers, timeout=5)
    #     result = res.json()
    #     data = result["data"]["page"]["pageComponents"]["pdpTechSpecs"]["technical_specifications"]

    #     return data
