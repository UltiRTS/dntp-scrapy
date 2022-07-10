# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DntpScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    map_name = scrapy.Field()
    map_url = scrapy.Field()
    minimap_filename = scrapy.Field()
    map_filename = scrapy.Field()
    map_hash = scrapy.Field()
