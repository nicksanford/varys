# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SephoraProduct(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    sephora_id = scrapy.Field()
    image_url = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    scraped_at = scrapy.Field()
    inserted_at = scrapy.Field()
    updated_at = scrapy.Field()

class SephoraReview(scrapy.Item):
    sephora_id = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()
    review_json = scrapy.Field()
    scraped_at = scrapy.Field()
    inserted_at = scrapy.Field()
    updated_at = scrapy.Field()
