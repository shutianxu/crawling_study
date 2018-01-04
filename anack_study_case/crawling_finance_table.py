# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 09:37:36 2017

@author: 1707500
"""

import requests
from requests.exceptions import RequestException
import re
import json
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}

def get_one_page(url):
    try:
        response = requests.get(url,headers = headers)
        response.encoding = 'GB2312'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


# =============================================================================
# def parse_one_page_zhengze(html):
#     try:    
#         pattern = re.compile('>(.*?)".*?>(.*?)</td><td',re.S)
#         items = re.findall(pattern,html)
#     except:
#         pass
#     print(items)
# =============================================================================
    
    
def parse_one_page(html):
    try:
        soup = BeautifulSoup(html,'html5lib')
        l = soup.select('table#BalanceSheetNewTable0')
        ls = l[0].tbody
        lls = ls.select('td')
        stock_raw_data = [] #记得初始化，否则append会一直叠加
        stock_data=[]
        data = []
        senson_one=[]
        senson_two=[]
        senson_three=[]
        senson_four=[]
        for l in lls:
            if (l.get_text().strip()) != '流动资产' and (l.get_text().strip()) != '非流动资产' and (l.get_text().strip()) != '流动负债' and (l.get_text().strip()) != '非流动负债' and (l.get_text().strip()) != '所有者权益':
                stock_raw_data.append(l.get_text().strip())
        #print(stock_raw_data)
        stock_data = stock_raw_data[4:]
        dates = stock_raw_data[1:4]
        dates = list(reversed(dates))
        features = stock_data[::4]
        senson_one = stock_data[1::4]
        senson_two = stock_data[2::4]
        senson_three = stock_data[3::4]
        
        data.append(senson_one)
        data.append(senson_two)
        data.append(senson_three)

        df = pd.DataFrame(data, index=dates, columns= features)
        return df
# =============================================================================
#         
#         len(stock_raw_data)
# 
#         code = stock_raw_data[::4]
#         name = stock_raw_data[1::4]
#         quantity = stock_raw_data[2::4]
#         rate = stock_raw_data[3::4]
# 
#         length = len(code)
#         i = 0
#         while i < length:
#             if(name[i] == self.stock_name):
#                 yt_code.append(code[i])
#                 yt_name.append(name[i])
#                 yt_quantity.append(quantity[i])
#                 a = rate[i]
#                 a = a[:-1]
#                 a = float(a)
#                 yt_rate.append(a)
#             i += 1
# =============================================================================
    except:
        #仅供测试使用
        pass
# =============================================================================
#         print(self.stock_name + 'creat dataframe error!!')
#         yt_rate.append(0)
#         yt_code.append(0)
#         yt_name.append(0)
#         yt_quantity.append(0)
#         break
#          
# 
# =============================================================================

# =============================================================================
# 
# def write_to_file(content):
#     with open('D:\document\crawling\shengpingjia1.txt','a',encoding = 'utf-8') as f:
#         f.write(content  +'\n')
#         f.close()
# 
# =============================================================================



def main():
    url = 'http://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/600660/ctrl/2017/displaytype/4.phtml'
    html = get_one_page(url)      
    df = parse_one_page(html)
    df.to_csv('D:\document\crawling\caibao.csv') 
    print(df)
# =============================================================================
#     for j in parse_one_page(html):
#         a.append(j)
# for k in a[::2]:
#     koubei_url = 'http://car.bitauto.com/tusheng/koubei/'+str(k)+'/'
#     koubei_html = get_one_page(koubei_url)
#     parse_one_page_zonghe(koubei_html)
# =============================================================================
        
    
if __name__ == '__main__':
    main()
    