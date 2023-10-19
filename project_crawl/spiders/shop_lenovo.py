import scrapy


class ShopLenovoSpider(scrapy.Spider):
    name = "shop_lenovo"
    # allowed_domains = ["www.lenovo.com"]
    start_urls = [
        "https://www.lenovo.com/us/en/search?fq=&text=Laptops&rows=60&sort=relevance&fsid=1&display_tab=Products",
        # "https://www.lenovo.com/us/en/search?fq=&text=Desktops&rows=60&sort=relevance&fsid=1&display_tab=Products",
        "https://www.lenovo.com/us/en/search?fq={!ex=prodCat}lengs_Product_facet_ProdCategories:PCs%20Tablets&text=Desktops&rows=60&sort=relevance&display_tab=Products"
        "https://www.lenovo.com/us/en/search?fq=&text=Docking&rows=60&sort=relevance&fsid=1&display_tab=Products",
        ]

    def parse(self, response):
        pass
