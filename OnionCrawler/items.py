# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class OnionCrawlerScraperItem(scrapy.Item):
    # The source URL
    url_from = scrapy.Field()
    # The destination URL
    url_to = scrapy.Field()