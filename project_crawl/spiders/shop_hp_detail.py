from project_crawl.share.models import Product
from project_crawl.share.utils import init_logging, print_line, get_settings, get_db_connect_string, is_env_production
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from types import SimpleNamespace

import json
import scrapy


class ShopHpDetailSpider(scrapy.Spider):
    name = "shop_hp_detail"
    # allowed_domains = ["www.hp.com"]
    start_urls = [
        # "https://www.hp.com/us-en/shop/app/api/web/graphql/page/pdp%2Fhp-envy-x360-2-in-1-laptop-15t-fe000-156-77x87av-1/async",
        # "https://www.hp.com/us-en/shop/app/api/web/graphql/page/pdp%2Fomen-gaming-laptop-16t-wf000-161-76w27av-1/async"
    ]

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
    products = []

    def __init__(self, name=None, **kwargs):
        init_logging()
        db_connect_string = get_db_connect_string()
        engine = create_engine(f"sqlite:///{db_connect_string}", echo=True)

        with Session(engine) as session:
            statement = select(Product).where(Product.Spec_Json == None).limit(1)
            self.products = session.scalars(statement).all()

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
        print_line(response)
        result = response.json()

        try:
            # TODO:
            # data_json = json.loads(result["data"], object_hook=lambda x: SimpleNamespace(**x))
            # data = data_json.data.page.pageComponents.pdpTechSpecs.technical_specifications
            data = result["data"]["page"]["pageComponents"]["pdpTechSpecs"]["technical_specifications"]

            db_connect_string = get_db_connect_string()
            engine = create_engine(f"sqlite:///{db_connect_string}", echo=True)

            with Session(engine) as session:
                self.products = session.execute(update(Product), [
                    { "Id": item.Id, "Spec_Json": str(data) }
                ])
                session.commit()

        except Exception:
            pass
