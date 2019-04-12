# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    shop_name = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    comment_count = scrapy.Field()
    good_count = scrapy.Field()
    general_count = scrapy.Field()
    poor_count = scrapy.Field()
    show_count = scrapy.Field()


