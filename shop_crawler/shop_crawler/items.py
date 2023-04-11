# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    characteristics = scrapy.Field()
    image = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    breadcrumbs = scrapy.Field()