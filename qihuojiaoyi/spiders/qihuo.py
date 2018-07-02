# -*- coding: utf-8 -*-
import scrapy
from qihuojiaoyi.items import QihuojiaoyiItem
import datetime


class QihuoSpider(scrapy.Spider):
    name = 'qihuo'
    #重构构造方法，用于命令行输入开始日期参数，方便爬取
    def __init__(self , date=None , *args , **kwargs):#date为用户设置的开始爬取的日期格式为yyyymmdd
        super(QihuoSpider , self).__init__(*args , **kwargs)
        print('*********************启动爬虫**************************')
        self.start_date = date
        if self.is_past_date(date):#输入的日期成为过去，就是说有数据可以爬取
            self.start_urls = ['http://www.shfe.com.cn/data/dailydata/kx/kx' + self.start_date + '.dat']
            print(self.start_urls)
        else:#输入的是未来日期，没有数据不能爬取
            print('您输入的日期上尚未到来，数据爬取失败……')
            self.close()
        self.allowed_domains = ['http://www.shfe.com.cn/']
    def get_next_day(self , date):
        '''
        输入一个日期（字符串日期，或者日期格式），输出下一工作日字符串类型的日期
        :return:
        '''
        if type(date)==datetime.datetime :#如果传入的参数是日期类型
            day_of_week = date.weekday()
            if day_of_week <= 3 or day_of_week == 6:
                next_day = date + datetime.timedelta(days = 1)
            elif day_of_week == 4:
                next_day = date + datetime.timedelta(days = 3)
            elif day_of_week == 5:
                next_day = date + datetime.timedelta(days = 2)
            print('日期类型')
        elif type(date)==str :#如果传入的参数是字符串类型
            date = datetime.datetime.strptime(date, "%Y%m%d")#转换为日期类型
            day_of_week = date.weekday()
            if day_of_week <= 3 or day_of_week == 6:
                next_day = date + datetime.timedelta(days = 1)
            elif day_of_week == 4:
                next_day = date + datetime.timedelta(days = 3)
            elif day_of_week == 5:
                next_day = date + datetime.timedelta(days = 2)
        if next_day >= datetime.datetime.now():#如果下一工作日超过今天日期，返回False
            return False
        else:
            next_date = next_day.strftime("%Y%m%d")
            return next_date

    def is_past_date(self , date):
        '''
        输入一个字符型日期date，判断该日期相较于当前日期是否过去
        :return:
        '''

        if date:
            ming_date = datetime.datetime.strptime(date, "%Y%m%d")#转换为日期类型
            now_date = datetime.datetime.now()
            if ming_date < now_date:
                return True
            else:
                return False
        else:
            return False

    def parse(self, response):
        try:#使用异常处理，若是发生403.404等一些列异常，跳过继续下一页爬取，可防止爬虫因意外退出
            item = QihuojiaoyiItem()
            html_dict = eval(response.body)#将字符串类型网页转换为字典，方便提取数据
            initial_data_list = html_dict.get("o_curinstrument")#包含每一条数据（包括非铜材料的数据）的一个list,每一个元素都是字典
            for each in initial_data_list:
                if(each.get("PRODUCTSORTNO")==10):
                    item['commodity_variety'] = each.get("DELIVERYMONTH"),
                    item['stock_date'] = self.start_date ,
                    item['pre_settlement'] = each.get("PRESETTLEMENTPRICE"),
                    item['open_price'] = each.get("OPENPRICE"),
                    item['highest_price'] = each.get("HIGHESTPRICE"),
                    item['minimum_price'] = each.get("LOWESTPRICE"),
                    item['closing_price'] = each.get("CLOSEPRICE"),
                    item['reference_price'] = each.get("SETTLEMENTPRICE"),
                    item['ups_and_downs_1'] = each.get("ZD1_CHG"),
                    item['ups_and_downs_2'] = each.get("ZD2_CHG"),
                    item['transaction_hand'] = each.get("VOLUME"),
                    item['holding_hands'] = each.get("OPENINTEREST"),
                    item['transformation'] = each.get("OPENINTERESTCHG")
                    print('*************************{}***********************'.format(item['stock_date']))
                    yield item
        except Exception as e:
            print('发生异常，{}信息爬取失败：{}'.format(self.start_date , e))
        finally:
            self.start_date = self.get_next_day(self.start_date)#获取下一工作日
            if self.start_date:
                next_url = 'http://www.shfe.com.cn/data/dailydata/kx/kx' + self.start_date + '.dat'#构造下一页地址
                yield scrapy.Request(url = next_url , callback = self.parse, dont_filter=True)#这里的,dont_filter=True)参数一定不能丢，否则只能回调一次