import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

data = pd.read_excel('codes.xlsx', dtype={'codes': str}, index=False)
codes = data['codes']
totle_numbers = data['numbers']

driver = webdriver.Chrome(executable_path='D:\linjiafengyang\Code\Python\chromedriver')
url = 'http://guba.eastmoney.com/list,{code},1,f_{page}.html'

for code, totle_number in zip(codes, totle_numbers):
    newsary = []
    ##对每个页面进行循环抓取
    for i in range(1, totle_number+1):    
        page_content = url.format(code=code, page=i)
        print(page_content)
        driver.implicitly_wait(30)
        driver.get(page_content)
        #res.encoding="utf-8"
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        result = soup.select('.articleh .l3 a')

        ##从该页面中，获取全部新闻的URL
        for index in result:
            news_url = "http://guba.eastmoney.com"+ index['href']
            
            ##从每个新闻的URL中，抓取新闻内容，包括标题，内容，用户昵称，发布时间       
            content = requests.get(news_url)
            content.encoding="utf-8"
            content_soup = BeautifulSoup(content.text, 'html.parser')
            t = content_soup.select('#zwconttbt')
            if len(t) > 0:
                title = t[0].text.strip()
            b = content_soup.select('#zwconbody .stockcodec')
            if len(b) > 0:
                body = b[0].text.strip()
            u = content_soup.select('#zwconttbn a')
            if len(u) > 0:
                user = u[0].text
            pt = content_soup.select('.pager .zwfbtime')
            if len(pt) > 0:
                post_time= pt[0].text
            
            ##把数据保存到Pandas对象中
            newsary.append({'title':title, 'body':body , 'user': user , 'time': post_time})
            time.sleep(3)
        print(">==========<")
        time.sleep(10)

    ##修改保存的文件名
    daf = pd.DataFrame(newsary)        
    daf.to_excel(str(code+".xlsx"))