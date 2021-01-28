#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import urllib.request
import requests
from multiprocessing.dummy import Pool
from lxml import etree
import os


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  OK  ---")

    else:
        print("---  There is this folder!  ---")


# 通过目标网站主页爬取车型及车型链接
def scrapy(item):
    headers = {'accept': '*/*'}
    url = f'https://www.autohome.com.cn/grade/carhtml/{item}.html'
    html = requests.get(url, headers=headers)
    html2 = etree.HTML(html.text)
    if len(html.text) > 0:
        # 车型
        car_model = html2.xpath('//*[@class="greylink"]/text()')

        # 车型链接
        car_link = html2.xpath('//*[@class="greylink"]/@href')
        for i in range(0, len(car_model)):
            write_content.append({'链接': car_link[i]
                                     , '车型': car_model[i]
                                  })
    else:
        return []
    return write_content


def spider(url):
    req = requests.get('https:' + url)
    req2 = etree.HTML(req.text)

    # 车型2
    car_name = req2.xpath('/html/body/div[1]/div[3]/div[2]/span[2]/text()')
    car_name = ''.join(car_name)

    # 品牌
    brand = req2.xpath('/html/body/div[1]/div[3]/div[2]/a[2]/text()')
    brand = ''.join(brand)

    # 品牌logo
    brand_logo = req2.xpath('/html/body/div[1]/div[3]/div[3]/div[1]/div[1]/img/@src')
    brand_logo = ''.join(brand_logo)

    img = os.path.exists(common_path + 'brand/' + brand + '.jpg')
    if not img:
        f = open(common_path + 'brand/' + brand + ".jpg", 'wb')
        f.write((urllib.request.urlopen(brand_logo)).read())
        os.makedirs(common_path + 'car_type/' + brand)

    # 车型样图
    car_img = req2.xpath('//*[@class="pic-main"]/a/picture/source/@srcset')
    car_img = ''.join(car_img)
    b = car_img.split(',')[0]
    c = b.replace(' ', '%20')

    img2 = os.path.exists(common_path + 'car_type/' + brand + '/' + car_name + '.jpg')
    if not img:
        f = open(common_path + 'car_type/' + brand + '/' + car_name + ".jpg", 'wb')
        with urllib.request.urlopen('https:' + c) as response:
             f.write(response.read())
        
        #f.write((urllib.request.urlopen('https:' + c)).read())

    write_content2.append({'链接': url
                              , '车型2': car_name
                              , '品牌': brand
                              , '品牌logo': brand_logo
                              , '车型样图': car_img
                           })
    return write_content2


# 第一步：输入默认路径
common_path = "qichezhijia/"

# 第二步：创建品牌图片存储路径
file = "qichezhijia/brand/"
mkdir(file)

# 第二步半：创建车型图片存储路径
file2 = "qichezhijia/car_type/"
mkdir(file2)

# 第三步： 跑 链接+车名
index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
         'W', 'X', 'Y', 'Z']
write_content = []
# 创建10个线程
pool = Pool(10)
# 爬取的页码放在一个列表里 [1,2,3,...,1000]
orign_num = [x for x in index]
# 通过映射返回结果列表
result = pool.map(scrapy, orign_num)
df = pd.DataFrame(write_content)

# 第四步： 跑 品牌、品牌logo、balabala
write_content2 = []
# 创建10个线程
pool = Pool(10)
# 通过映射返回结果列表
result = pool.map(spider, df["链接"])


df2 = pd.DataFrame(write_content2)
df3 = pd.merge(df, df2, on='链接', how='left')