# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class WeiboItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    table_name = 'weibo'

    weibo_id = Field()
    weibo_url = Field()
    weibo_content = Field()
    posted_at = Field()
    posted_from = Field()

    user_id = Field()
    user_name = Field()
    user_gender = Field()
    district = Field()
