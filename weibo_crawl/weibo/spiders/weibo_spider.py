# -*- coding: utf-8 -*-
import datetime
import json
import random
import re

import requests
import scrapy
import time

from weibo.items import WeiboItem


# def random_Time():
#     a1 = (2011, 1, 1, 0, 0, 0, 0, 0, 0)
#     a2 = (2017, 12, 31, 23, 59, 59, 0, 0, 0)
#
#     start = time.mktime(a1)
#     end = time.mktime(a2)
#
#     t = random.randint(start, end)
#     date_touple = time.localtime(t)
#     date = time.strftime("%Y%m%d", date_touple)
#     return int(date)


class WeiboSpiderSpider(scrapy.Spider):
    name = 'weibo_spider'
    allowed_domains = ['weibo.cn']
    start_urls = 'https://weibo.cn/search/mblog'
    max_page = 100
    # endtime = random_Time()
    # date_list = []

    # def __init__(self):
    #     begin = datetime.date(2011, 1, 1)
    #     end = datetime.date(2018, 3, 31)
    #
    #     day = end
    #     delta = datetime.timedelta(days=1)
    #     while day >= begin:
    #         self.date_list.append(day.strftime('%Y%m%d'))
    #         day -= delta

    '''
    url: keyword=关键词
         filter=hasori  原创微博
         starttime=20100522     开始时间
         endtime=20150522       截止时间
    
    parse_index中的is_forward不需要了，直接使用微博自带的filter
        is_forward = bool(weibo.xpath('.//span[@class="cmt"]').extract_first())
    '''

    def start_requests(self):
        keyword = '吃了'
        url = '{url}?keyword={keyword}&filter=hasori&starttime=20100101'.format(url=self.start_urls, keyword=keyword)

        # for endtime in self.date_list:
        for page in range(self.max_page + 1):
            data = {
                'mp': str(self.max_page),
                'page': str(page),
                # 'endtime': endtime
            }
            yield scrapy.FormRequest(url, callback=self.parse_index, formdata=data)

    def parse_index(self, response):
        weibos = response.xpath('//div[@class="c" and contains(@id, "M_")]')
        for weibo in weibos:
            # 微博详情页
            detail_url = weibo.xpath('.//a[contains(., "评论[")]//@href').extract_first()

            # 添加来自
            posted_from = weibo.xpath('.//span[@class="ct"]/a/text()').extract_first()
            if posted_from is None:
                posted_from = weibo.xpath('.//span[@class="ct"]/text()').extract_first()
                try:
                    posted_from = re.search('来自(.*)', posted_from).group(1)
                except AttributeError as e:
                    posted_from = None

            # 添加位置信息
            dis_url = response.xpath('.//a[@class="nk"]/@href').extract_first()
            try:
                res = requests.get('http://127.0.0.1:5000/weibo/random')
                if res.status_code == 200:
                    temp_cookies = eval(res.text)
            except ConnectionError:
                temp_cookies = None
            res_dis = requests.get(dis_url, cookies=temp_cookies).content.decode('utf-8', errors='ignore')
            district = re.search('[男|女]/(.*?)\&', res_dis).group(1).rstrip()

            request = scrapy.Request(detail_url, callback=self.parse_detail)
            request.meta['posted_from'] = posted_from
            request.meta['district'] = district
            yield request

    def parse_detail(self, response):
        posted_from = response.meta['posted_from']
        district = response.meta['district']

        # 微博id
        weibo_id = re.search('comment\/(.*?)\?', response.url).group(1)
        weibo_url = response.url
        weibo_content = ''.join(response.xpath('//div[@id="M_"]//span[@class="ctt"]//text()').extract())
        posted_at = response.xpath('//div[@id="M_"]//span[@class="ct"]//text()').extract_first(default=None)

        user_url = response.xpath('//div[@id="M_"]/div[1]/a/@href').extract_first()
        user_id = user_url.split('/')[-1]
        user_name = response.xpath('//div[@id="M_"]/div[1]/a/text()').extract_first(default=None)
        user_gender = response.xpath('//div[@id="M_"]/div/a[contains(., "关注")]/text()').extract_first()

        weibo_item = WeiboItem()
        weibo_item['weibo_id'] = weibo_id
        weibo_item['weibo_url'] = weibo_url
        weibo_item['weibo_content'] = weibo_content
        weibo_item['posted_at'] = posted_at
        weibo_item['posted_from'] = posted_from

        weibo_item['user_id'] = user_id
        weibo_item['user_name'] = user_name
        weibo_item['user_gender'] = user_gender
        weibo_item['district'] = district

        yield weibo_item
