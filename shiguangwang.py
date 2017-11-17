# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 11:45:12 2017

@author: 1707500
"""


import requests
from requests.exceptions import RequestException
import re
import json

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code ==200:
            return response.text
        return None
    except RequestException:
        return None
    
def parse_one_page(html):
    pattern = re.compile('<div class="number"><em>(\d+)</em></div>.*?<h2 class="px14 pb6">.*?target="_blank">(.*?)&nbsp;(.*?)</a></h2>.*?<p>.*?target="_blank">(.*?)</a></p>.*?<p>.*?target="_blank">(.*?)</a>.*?target="_blank">(.*?)</a>.*?target="_blank">(.*?)</a>.*?target="_blank">(.*?)</a>.*?<p class="mt3">(.*?)</p>.*?class=total>(\d+)</.*?class=total2>(.*?)</',re.S)
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
               'year':item[2],
               'daoyan':item[3],
               'zhuyan':item[4]+','+item[5],
               'type':item[6]+','+item[7],
               'jieshao':item[8],
               'fenshu':item[9]+item[10]
                }
#    print(items)
def write_to_file(content):
    with open('D:\document\crawling\shiguangwang.txt','a',encoding = 'utf-8') as f:
        f.write(json.dumps(content,ensure_ascii = False)  +'\n')
        f.close()
    
def main():
    for i in range(10):
        if i == 0:
            url = 'http://www.mtime.com/top/movie/top100/'
        else:
            url = 'http://www.mtime.com/top/movie/top100/index-'+str(i+1)+'.html'
        html = get_one_page(url)
        for item in parse_one_page(html):
            print(item)
            write_to_file(item)
if __name__ == '__main__':
    main()
    
    
    