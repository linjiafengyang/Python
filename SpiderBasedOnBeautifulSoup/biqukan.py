# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')  

if __name__ == '__main__':
    #target = 'http://www.biqukan.com/1_1094/5403177.html'
    server = 'http://www.biqukan.com/'
    target = 'http://www.biqukan.com/1_1094/'#一念永恒的目录
    req = requests.get(target)
    html = req.text
    div_bf = BeautifulSoup(html, 'lxml')
    div = div_bf.find_all('div', class_ = 'listmain')
    #print (div[0])
    a_bf = BeautifulSoup(str(div[0]), 'lxml')
    a = a_bf.find_all('a')
    for each in a[15:]:#去除不必要的章节（提示新更新的章节）
        #print (each.string, server + each.get('href'))
        content_req = requests.get(server + each.get('href'))#每一章节对应的url
        content_html = content_req.text#章节内容html
        bf = BeautifulSoup(content_html, 'lxml')
        texts = bf.find_all('div', class_ = 'showtxt')#返回的是一个列表
        #print (texts[0].text.replace('\xa0'*8, '\n\n'))#替换空格，以回车代替
        with open('一念永恒.txt', 'a', encoding='utf-8') as f:
            f.write(each.string + '\n')#章节名称
            f.writelines(texts[0].text.replace('\xa0'*8, '\n\n'))
            f.write('\n\n')
