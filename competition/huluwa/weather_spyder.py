#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 22 13:50:26 2018

@author: linzizhan
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time

def day_weather(year, month, day):
    url = 'https://tianqi.911cha.com/haidian/%d-%d-%d.html'%(year, month, day)
    header = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
                }
    response = requests.get(url, headers = header).text
    data = BeautifulSoup(response, 'html.parser')
    wea = data.find('div', {'class':'leftbox'}).find('table', {'class':'center'}).find_all('tr')
    res = {'day':[], 'time':[], 'weather':[], 'temp':[], 'shidu':[], 'wind':[], 'rain':[], 'body_temp':[]}
    for i in wea[1:]:
        idata = i.find_all('td')
        res['day'].append('%d%02d%02d'%(year, month, day))
        res['time'].append(i.find('th').text)
        res['weather'].append(idata[1].text)
        res['temp'].append(idata[2].text)
        res['shidu'].append(idata[3].text)
        res['wind'].append(idata[6].text)
        res['rain'].append(idata[7].text)
        res['body_temp'].append(idata[8].text)
    df = pd.DataFrame(res, columns=['day','time','weather','temp','shidu','wind','rain','body_temp'])
    time.sleep(10)
    return df

stamp = datetime.datetime(2017, 1, 1, 0, 0, 0)
df = pd.DataFrame()
while stamp < datetime.datetime(2018, 1, 1, 0, 0, 0):
    year = stamp.year
    month = stamp.month
    day  = stamp.day
    print(year, month, day)
    df = df.append(day_weather(year, month, day))
    stamp = stamp + datetime.timedelta(days=1)
df.to_csv('weather.csv', index = False)