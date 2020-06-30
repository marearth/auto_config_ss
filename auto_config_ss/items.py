# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SiteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    server = scrapy.Field()
    server_ipv6 = scrapy.Field()
    server_port = scrapy.Field()
    local_address = scrapy.Field()
    local_port = scrapy.Field()
    password = scrapy.Field()
    group = scrapy.Field()
    method = scrapy.Field()
    obfsparam = scrapy.Field()
    protoparam = scrapy.Field()



