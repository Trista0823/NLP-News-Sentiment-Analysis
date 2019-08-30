# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import time
import lxml
import pandas as pd
import numpy as np
import datetime
from snownlp import SnowNLP


#情绪计算      
def sentiment_compute(sentences, stop_words):
    sentiments = []
    for sentence in sentences:
        sentence = sentence.replace('\n', '')
        sentence = sentence.replace(' ', '')
        for stop_word in stop_words:
            sentence = sentence.replace(stop_word, '')
        try:
            sentiment = SnowNLP(sentence).sentiments
            sentiments.append(sentiment)
        except:
            pass
    return sentiments

#新闻爬取
def news_crawl(keyword, bt, et, pages):
    all_news = []
    for page in range(pages):
        url = 'http://news.baidu.com/ns?from=news&cl=2&pn=' + str(page*20) + '&bt=' + str(bt) + '&et=' + str(et) + '&q1=' + str(keyword) + '&q4=&mt=0&lm=&s=2&tn=newsdy&ct1=1&ct=1&rn=20'
        response = requests.get(url).text
        response = response.replace('<em>', '')
        response = response.replace('</em>', '')

        data = lxml.etree.HTML(response.lower())
        title = data.xpath('//h3[@class="c-title"]/a/text()')    
        abstract = data.xpath('//div[@class="c-summary c-row "]/text()|//div[@class="c-span18 c-span-last "]/text()')
        news = abstract + title
        all_news += news
    return all_news
        
keywords = ['小额贷款', '消费金融', '互联网金融',  '小微企业', '汽车金融', '保险科技', '电子银行']
pages = 3
sentiments = {}
t0 = datetime.datetime(2018, 9, 1, 0, 0, 0)
index = []
peroids = 14

for keyword in keywords:
    sentiments[keyword] = []
    for i in range(peroids):
        t1 = t0 + datetime.timedelta(days = i)
        t2 = t1 + datetime.timedelta(days = 1)
        t1 = time.strptime(str(t1), "%Y-%m-%d %H:%M:%S")
        t2 = time.strptime(str(t2), "%Y-%m-%d %H:%M:%S")
        index.append(str(t1.tm_mon)+'-'+str(t1.tm_mday))
        bt = time.mktime(t1)
        et = time.mktime(t2)
        news = news_crawl(keyword, bt, et, pages)
        sentiment = sentiment_compute(news, keywords)      
        sentiments[keyword].append(np.mean(sentiment))  
df = pd.DataFrame(sentiments, index = index[0:14])
df.to_excel('./'+str(t0)+'sum.xlsx')
print(df)