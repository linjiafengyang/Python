# -*-encoding:utf-8-*-
import requests
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')         #改变标准输出的默认编码

from bs4 import BeautifulSoup 

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
r = requests.get('https://qiushibaike.com')
content = r.text
#print (content)
soup = BeautifulSoup(content, 'lxml')
divs = soup.find_all(class_ = 'article block untagged mb15 typs_hot')
print (divs)
for div in divs:
    joke = div.span.get_text()
    print(joke)
    print('------')
