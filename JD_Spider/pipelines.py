# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class JdSpiderPipeline(object):
    def __init__(self):
        #  localhost
        self.connect = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='123456',
            db='jd',
            port=3306,

        )
        self.cursor = self.connect.cursor()


    def process_item(self, item, spider):

        self.cursor.execute('''
        insert into jd_phone(id,title,url,shop_name,price,brand,model,comment_count,good_count,general_count,poor_count,show_count) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(item['id'],item['title'],item['url'],item['shop_name'],item['price'],item['brand'],item['model'],item['comment_count'],item['good_count'],item['general_count'],item['poor_count'],item['show_count']))

        self.connect.commit()
        return item


    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()
