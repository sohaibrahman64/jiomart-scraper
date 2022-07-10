# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst


def remove_currency_symbol(value):
    return value.replace('\u20b9 ', '')


class JiomartscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # id = scrapy.Field(output_processor=Join())
    name = scrapy.Field(output_processor=Join())
    selling_price = scrapy.Field(input_processor=MapCompose(remove_currency_symbol), output_processor=Join())
    original_price = scrapy.Field(input_processor=MapCompose(remove_currency_symbol), output_processor=Join())
    image = scrapy.Field(output_processor=Join())


class SmartwatchesscraperItem(scrapy.Item):
    name = scrapy.Field(output_processor=Join())
    rating = scrapy.Field(output_processor=Join())
    selling_price = scrapy.Field(input_processor=MapCompose(remove_currency_symbol), output_processor=Join())
    original_price = scrapy.Field(input_processor=MapCompose(remove_currency_symbol), output_processor=Join())
    discount = scrapy.Field(output_processor=Join())
    image = scrapy.Field(output_processor=Join())
