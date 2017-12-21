# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 15:07:04 2017

@author: 1707500
"""

import itchat
import numpy as np
import pandas as pd
from collections import defaultdict
import re
import jieba
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import PIL.Image as Image


itchat.login()
friends = itchat.get_friends(update=True)[0:]



#男女比例
male = female = other = 0
    
for i in friends[1:]:
    sex = i["Sex"]
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
        other +=1
#计算朋友总数
total = len(friends[1:])
#打印出自己的好友性别比例
print("男性好友： %.2f%%" % (float(male)/total*100) + "n" +
"女性好友： %.2f%%" % (float(female) / total * 100) + "n" +
"不明性别好友： %.2f%%" %(float(other) / total * 100))



#自己微信好友的城市分布

#定义一个函数，用来爬取各个变量
def get_var(var):
    variable = []
    for i in friends:
        value = i[var]
        variable.append(value)
    return variable


#调用函数得到各变量，并把数据存到csv文件中，保存到桌面
NickName = get_var("NickName")
Sex = get_var('Sex')
Province = get_var('Province')
City = get_var('City')
Signature = get_var('Signature')
data = {'NickName': NickName, 'Sex': Sex, 'Province': Province,
'City': City, 'Signature': Signature}
frame = pd.DataFrame(data)
frame.to_csv('E:\workspace\wechat\data.csv', index=True)


#自己微信好友个性签名的自定义词云图



tList = []
for i in friends:
    signature = i["Signature"].replace(" ", "").replace("span", "").replace("class", "").replace("emoji", "")
    rep = re.compile("1f\d.+")
    signature = rep.sub("", signature)
    tList.append(signature)
    # 拼接字符串
    text = "".join(tList)
# jieba分词
wordlist_jieba = jieba.cut(text, cut_all=True)
wl_space_split = " ".join(wordlist_jieba)
# wordcloud词云
print(wl_space_split)
wc = WordCloud(font_path='D:\simhei.TTF', background_color="white",width=2000, height=860, margin=2)
# generate word cloud
wc.generate(text)
# store to file
wc.to_file('result.png') 
#调节大小
# show
plt.imshow(wc)
plt.axis("off")
# plt.figure()
# plt.imshow(alice_mask, cmap=plt.cm.gray)
# plt.axis("off")
plt.show()


