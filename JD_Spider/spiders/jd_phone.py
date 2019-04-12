# -*- coding: utf-8 -*-
import scrapy
import json
from JD_Spider.items import JdSpiderItem
import datetime

class JdPhoneSpider(scrapy.Spider):
    name = 'jd_phone'
    allowed_domains = ['jd.com']
    start_urls = ['http://jd.com/']
    #  需要爬取的类目
    keyword = '手机'
    #  商品列表初始页
    page = 1
    #  商品列表页的初始页
    top_thirty_url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&cid3=655&page=%d&s=1&click=0'
    later_thirty_url = 'https://search.jd.com/s_new.php?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&cid2=653&cid3=655&page=%d&s=27&scrolling=y&log_id=1554788586.68322&tpl=3_M&show_items=%s'
    comment_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=%s'

    def start_requests(self):
        #  请求商品列表页的第一页，获取的商品列表页只包含前30个物品
        yield scrapy.Request(url=self.top_thirty_url%(self.keyword,self.page),callback=self.parse)



    def parse(self, response):
        #  id_list用于获取商品列表页前30个商品id
        id_list = []
        #  获取商品列表页前30个商品的gl-item列表
        gl_items = response.xpath('//li[@class="gl-item"]')
        for gl_item in gl_items:
            price = gl_item.xpath('./div[@class="gl-i-wrap"]/div[@class="p-price"]/strong/i/text()').extract_first()

            url = gl_item.xpath('./div[@class="gl-i-wrap"]/div[@class="p-name p-name-type-2"]/a/@href').extract_first()
            if url.startswith('//'):
                url = ''.join(['http:',url])
            id = gl_item.xpath('./@data-pid').extract_first()
            # print(price,url,id)
            id_list.append(id)
            #  回调到处理商品评论js页面的函数
            yield scrapy.Request(url=self.comment_url%(id),callback=self.parseComment,meta={'price':price,'url':url})

        if self.page <= 199:
            self.page += 1
            id_list = ','.join(id_list)

            #  回调到处理商品列表评论js页面的函数
            yield scrapy.Request(url=self.later_thirty_url%(self.keyword,self.page,id_list),callback=self.parseNext,headers={'Referer':response.url})


    def parseNext(self,response):
        gl_items = response.xpath('//li[@class="gl-item"]')
        for gl_item in gl_items:
            price = gl_item.xpath('./div[@class="gl-i-wrap"]/div[@class="p-price"]/strong/i/text()').extract_first()

            url = gl_item.xpath('./div[@class="gl-i-wrap"]/div[@class="p-name p-name-type-2"]/a/@href').extract_first()
            if url.startswith('//'):
                url = ''.join(['http:', url])
            id = gl_item.xpath('./@data-pid').extract_first()
            # print(price,url,id)
            #  回调到处理商品评论js页面的函数
            yield scrapy.Request(url=self.comment_url % (id), callback=self.parseComment,
                                 meta={'price': price, 'url': url})

        if self.page <= 199:
            self.page += 1
            yield scrapy.Request(url=self.top_thirty_url%(self.keyword,self.page),callback=self.parse)


    def parseComment(self,response):
        comment_dict = json.loads(response.text)['CommentsCount'][0]
        comment_count = comment_dict.get('CommentCount',0)
        good_count = comment_dict.get('GoodCount',0)
        general_count = comment_dict.get('GeneralCount',0)
        poor_count = comment_dict.get('PoorCount',0)
        show_count = comment_dict.get('ShowCount',0)
        id = comment_dict.get('SkuId',0)
        yield scrapy.Request(
            url=response.meta['url'],
            callback=self.parseDetail,
            meta={'price':response.meta['price'],'comment_count':comment_count,
                  'good_count':good_count,'general_count':general_count,'poor_count':poor_count,
                  'show_count':show_count,'id':id}
        )


    def parseDetail(self,response):
        title = response.xpath('//div[@class="sku-name"]/text()').extract_first().replace(' ','')
        if title == '\n':
            title = ''.join(response.xpath('//div[@class="sku-name"]/text()').extract()).strip()
        brand = response.xpath('//div[@class="inner border"]/div/a/text()').extract_first()
        model = response.xpath('//div[@class="item ellipsis"]/@title').extract_first()
        shop_name = response.xpath('//div[@class="name"]/a/text()').extract_first()
        url = response.url
        price = response.meta['price']
        id = response.meta['id']
        comment_count = response.meta['comment_count']
        good_count = response.meta['good_count']
        general_count = response.meta['general_count']
        poor_count = response.meta['poor_count']
        show_count = response.meta['show_count']
        # print(title)
        item = JdSpiderItem()
        item['id'] = id
        item['title'] = title
        item['url'] = url
        item['shop_name'] = shop_name
        item['price'] = price
        item['brand'] = brand
        item['model'] = model
        item['comment_count'] = comment_count
        item['good_count'] = good_count
        item['general_count'] = general_count
        item['poor_count'] = poor_count
        item['show_count'] = show_count
        # print(item)
        yield item
