# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os

class QihuojiaoyiPipeline(object):
    def __init__(self):
        self.file_path = 'date.csv'
        self.dict_key = ['类别','日期','前结算','今开盘','最高价','最低价', '收盘价','结算参考价','涨跌1','涨跌2','成交手','持仓手','变化']
        if not os.path.exists(self.file_path):
            self.file = open(self.file_path,'a',encoding='utf-8' , newline='')
            self.w=csv.writer(self.file)
            self.w.writerow(self.dict_key)
        else:
            self.file = open(self.file_path,'a',encoding='utf-8' , newline='')
            self.w=csv.writer(self.file)

    def process_item(self, item, spider):
        dict_values = [
            item['commodity_variety'][0],
            item['stock_date'][0],
            item['pre_settlement'][0],
            item['open_price'][0],
            item['highest_price'][0],
            item['minimum_price'][0],
            item['closing_price'][0],
            item['reference_price'][0],
            item['ups_and_downs_1'][0],
            item['ups_and_downs_2'][0],
            item['transaction_hand'][0],
            item['holding_hands'][0],
            item['transformation']]
        print(dict_values)
        self.w.writerow(dict_values)
        return item

    def close_spider(self , spider):
        self.file.close()
        self.file.flush()
        print('**********************关闭爬虫**********************')