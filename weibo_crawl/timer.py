# -*- coding: utf-8 -*-

# 主控制程序
# 启动爬虫 设置间隔爬取时间30分钟

import time
import os

if __name__ == '__main__':
    while True:
        os.system('scrapy crawl weibo_spider')
        print('----------------------sleep-----------------')
        time.sleep(1600)
