
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 14:55:53 2018

@author: 1707500
"""
import pandas as pd
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup



headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

def get_one_page(url):
    try:
        response = requests.get(url,headers = headers)
        if response.status_code ==200:
            return response.text
        return None
    except RequestException:
        return None


def parse_page(html):
        try:
            soup = BeautifulSoup(html,'html5lib')
            lls1 = soup.select('div#list-content div h3 a')
            lls2 = soup.select('div#list-content div p.details-item.tag')
            lls3 = soup.select('div#list-content div address')
            lls4 = soup.select ('div#list-content div strong')                  
            a=[]
            b=[]
            c=[]
            d=[]
            e=[]
            g=[]
            for x in lls1:
                a.append(x.get_text().strip())
            for y in lls2:
                b.append(y.get_text().strip().split("|")[0])
                c.append(y.get_text().strip().split("|")[1])
            for z in lls3:
                d.append(z.get_text().strip().split()[0])
                e.append(z.get_text().strip().split()[1])
            for l in lls4:
                g.append(l.get_text().strip())
            print(a)
            print(b)
            print(c)
            print(d)
            print(e)
            print(g)
            

        except:
            pass    
        
        df = pd.DataFrame({ 'ad' : a,
                         'type' : b,
                         'square' : c,
                         'name' : d,
                         'area' : e,
                         'price' : g })
        return(df)
a = pd.DataFrame()
for i in range(50):
    url = 'https://gy.zu.anjuke.com/fangyuan/p'+ str(i+1)+'1-x1/'
    html = get_one_page(url)
    df = parse_page(html) 
    a = pd.concat([a,df])

a.to_csv('D:/document/crawling/rent.csv')
    