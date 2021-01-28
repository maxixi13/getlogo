import init
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


homeurl = "https://car.m.autohome.com.cn/#pvareaid=6832756"
requesthome=requests.get(homeurl)
re=etree.HTML(requesthome.text)
aa=re.xpath(r'//li/div/img')
for i in aa:
    print(i.attrib)


# 创建基础文件夹
# mkdir(init.basedirlogo)
# mkdir(init.basedircar)
