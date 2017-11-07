# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MarketwatchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = scrapy.Field()
    company_code = scrapy.Field()
    company_exchange = scrapy.Field()
    company_sector = scrapy.Field()
    company_url = scrapy.Field()

class CoinBaseItem(scrapy.Item):
    fundbroker = scrapy.Field()
    fundcategory = scrapy.Field()
    fundname = scrapy.Field()
    fundlink = scrapy.Field()
    