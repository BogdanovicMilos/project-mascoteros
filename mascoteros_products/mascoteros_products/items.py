# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MascoterosProductsItem(scrapy.Item):
    product_name = scrapy.Field()
    product_short_description = scrapy.Field()
    product_description_details = scrapy.Field()
    product_rating = scrapy.Field()
    product_image_url = scrapy.Field()
