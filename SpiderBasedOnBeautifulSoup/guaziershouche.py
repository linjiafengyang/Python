# -*-encoding:utf-8-*-
from bs4 import BeautifulSoup
import requests
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')         #改变标准输出的默认编码

def detail(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    res_data = requests.get(url, headers = headers)
    soup = BeautifulSoup(res_data.text, 'lxml')
    titles = soup.select('body > div.list-wrap.js-post > ul > li > a > div.t')
    prices = soup.select('body > div.list-wrap.js-post > ul > li > a > div.t-price > p')
    for title, price in zip(titles, prices):
        data = {
            'title': title.get_text(),
            'price': price.get_text()
        }
        print(data)

def init():
    urls = ['https://www.guazi.com/shantou/buy/i{}/'.format(str(i)) for i in range(1, 10, 1)]
    for url in urls:
        detail(url)

if __name__ == '__main__':
    init()
