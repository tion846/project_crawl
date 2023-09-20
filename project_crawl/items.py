# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DictionaryItem(scrapy.Item):
    index = scrapy.Field()
    name = scrapy.Field()
    value = scrapy.Field()


class StoreAppItem(scrapy.Item):
    product_name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
