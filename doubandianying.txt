# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 15:55:21 2017

@author: 1707500
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 11:45:12 2017

@author: 1707500
"""


import requests
from requests.exceptions import RequestException
import re
import json


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
#Cookies = {'Cookie':''}

def get_one_page(url):
    try:
        response = requests.get(url,headers = headers)
        if response.status_code ==200:
            return response.text
        return None
    except RequestException:
        return None
    
def parse_one_page(html):
    pattern = re.compile('<em class="">(.*?)</em>.*?<span class="title">(.*?)</span>.*?<span class="title">&nbsp;/&nbsp;(.*?)</span>.*?<p class="">.*?导演: (.*?)&nbsp;&nbsp;&nbsp;(.*?)<br>.*?(\d+)&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp;(.*?)</p>.*?property="v:average">(.*?)</span>.*?<span class="inq">(.*?)</span>',re.S)
    items = re.findall(pattern,html)
    try:
        patternscore = re.compile('class=total2>(.*?)</',re.S)
        score = re.findall(patternscore,html)
    except:
        pass
    for item in items:
        yield{
               'rank':item[0], 
               'name':item[1],
               'English_name':item[2],
               'daoyan':item[3],
               'zhuyan':item[4],
               'nianfen':item[5],
               'guojia':item[6],
               'type':item[7],
               'fenshu':item[8],
               'jieshao':item[9]               
                }
#    print(items)
def write_to_file(content):
    with open('D:\document\crawling\doubanwang.txt','a',encoding = 'utf-8') as f:
        f.write(json.dumps(content,ensure_ascii = False)  +'\n')
        f.close()
    
def main():
        for i in range(250):
            url = 'https://movie.douban.com/top250?start='+str(i*25)+'&filter='
            html = get_one_page(url)
            for item in parse_one_page(html):
                print(item)
                write_to_file(item)
if __name__ == '__main__':
    main()
    
    
    