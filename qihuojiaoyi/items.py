# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QihuojiaoyiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    commodity_variety = scrapy.Field()#类别
    stock_date = scrapy.Field()#日期
    pre_settlement = scrapy.Field()#前结算
    open_price = scrapy.Field()#'今开盘'
    highest_price = scrapy.Field()#最高价
    minimum_price = scrapy.Field()#最低价
    closing_price = scrapy.Field()#收盘价
    reference_price = scrapy.Field()#参考价
    ups_and_downs_1 = scrapy.Field()# '涨跌1'
    ups_and_downs_2 = scrapy.Field()#'涨跌2'
    transaction_hand = scrapy.Field()#'成交手'
    holding_hands = scrapy.Field()#'持仓手'
    transformation = scrapy.Field()#'变化'
