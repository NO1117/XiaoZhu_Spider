#!/usr/bin/env/ python
# -*- coding:utf-8 -*-
# Author:Mr.Xu

import requests
import time
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class XiaoZhu():
    max_num = 9
    def __init__(self):
        self.ua = UserAgent()
        self.temp_url = "http://bj.xiaozhu.com/search-duanzufang-p{}-0/"
        # 获取随机的User-Agent
        self.headers = {
            "User-Agent": self.ua.random
        }
        self.parse_times = 0

    # 请求相应URL,并返回HTML文档
    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        # 请求前睡眠2秒
        time.sleep(2)
        if response.status_code != 200:
            print('parsing not success!--',url)
            # 请求不成功
            if self.parse_times < 3:
                # 重复请求三次
                self.parse_times += 1
                return self.parse_url(url)
            else:
                # 请求不成功, parse_times置为0
                self.parse_times = 0
                return None
        else:
            # 请求成功
            print('parsing success!--',url)
            # 请求成功, parse_times重置为0
            return response.text

    # 解析列表页面，并提取详情页的URL
    def parse_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        lis = soup.select("div#page_list > ul > li")
        for li in lis:
            # 提取详情页URL
            page_url = li.select("a")[0].attrs['href']
            page_html = self.parse_url(page_url)
            item = self.parse_page(page_html)
            self.save_item(item)

    # 解析详情页，并提取数据
    def parse_page(self, html):
        item_list = []
        soup = BeautifulSoup(html, 'lxml')
        temp_title = soup.select('div.pho_info > h4')[0].get_text()
        title = temp_title.replace('\n', '')
        address = soup.select("div.pho_info > p")[0].get('title')
        price = soup.select("div.day_l > span")[0].get_text()
        host_name = soup.select("a.lorder_name")[0].get_text()
        host_gender = soup.select("div.member_pic > div")[0].get('class')[0]
        item = dict(
            title=title,
            address=address,
            price=price,
            name=host_name,
            gender=self.gender(host_gender),
            )
        print(item)
        item_list.append(item)
        return item_list

    # 保存数据
    def save_item(self, item_list):
        with open('XiaoZhu.txt', 'a+', encoding='utf-8') as f:
            for item in item_list:
                json.dump(item, f, ensure_ascii=False, indent=2)
            f.close()
        print("Save success!")

    # 处理gender
    def gender(self, class_name):
        if class_name == 'member_ico1':
            return '女'
        if class_name == 'member_ico':
            return '男'

    # 逻辑实现
    def run(self):
        # 1.Find URL
        for i in range(1, self.max_num):
            url = self.temp_url.format(i)
            # 2.Send Request, Get Response
            html = self.parse_url(url)
            if html:
                self.parse_html(html)

if __name__=='__main__':
    spider = XiaoZhu()
    spider.run()

# 列表页规律分析
"""
http://bj.xiaozhu.com/search-duanzufang-p1-0/
http://bj.xiaozhu.com/search-duanzufang-p2-0/
http://bj.xiaozhu.com/search-duanzufang-p3-0/
...
http://bj.xiaozhu.com/search-duanzufang-pX-0/
"""


