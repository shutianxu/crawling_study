# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 16:57:16 2017

@author: 1707500
"""

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
    pattern = re.compile('<td>.*?<b>(.*?)</b>.*?</td>.*?<td>(\d{6})</td>',re.S)
    items = re.findall(pattern,html)
    try:
        patternscore = re.compile('<h4>(.*?)</h4>',re.S)
        score = re.findall(patternscore,html)
    except:
        pass
    
    print(items,score)
def write_to_file(content):
    with open('D:\document\crawling\shiguangwang.txt','a',encoding = 'utf-8') as f:
        f.write(json.dumps(content,ensure_ascii = False)  +'\n')
        f.close()
    
def main():
    for i in range(28):
        url = 'http://youbian.duoshitong.com/?id='+str(i+1)
        html = get_one_page(url)
        parse_one_page(html)
#        for item in parse_one_page(html):
 #           print(item)
#            write_to_file(item)
if __name__ == '__main__':
    main()