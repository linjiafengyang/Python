import requests
from urllib.parse import urlencode
import json
from hashlib import md5
from bs4 import BeautifulSoup
import re
import os
from requests.exceptions import RequestException
import pymongo
from config import *
from multiprocessing import Pool
from json.decoder import JSONDecodeError

# 数据库连接
client = pymongo.MongoClient(MONGO_URL, connect=False)
# 创建数据库
db = client[MONGO_DB]

# 抓取索引页
def get_page_index(offest, keyword):
    # 如何获得data:F12-network-F5-XHR-Headers-Query String Parameters
    data = {
        'offset': offest, # offest可变
        'format': 'json',
        'keyword': keyword, # keyword是可以自定义
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3
    }
    # urlencode可以把字典对象变成url的请求参数（from urllib.parse import urlencode）
    url = 'http://www.toutiao.com/search_content/?' + urlencode(data)
    
    try:
        response = requests.get(url)
        if response.status_code ==  200:
            return response.text
        return None
    except RequestException:
        print('请求异常')
        return None

# 分析索引页得到每一篇文章的url
def parse_page_index(html):
    try:
        # 转换成json对象
        data = json.loads(html)
        if data and 'data' in data.keys():
            # data这个对象非空 并且 这个对象里有叫'data'的key
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass

# 抓取详情页
def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求异常')
        return None

# 分析详情页
def parse_page_detail(html, url):
    # 利用BeautifulSoup得到每一篇文章的title
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    print(title)

    # 利用正则表达式得到图集链接的json数据
    # gallery原网页response数据如下
    # gallery: {"count":6,"sub_images":[{"url":"http:\/\/p3.pstatp.com\/origin\/39ff000320f6c9d365a2",
    # "width":1920,"url_list":[{"url":"http:\/\/p3.pstatp.com\/origin\/39ff000320f6c9d365a2"},{"url":"
    images_pattern = re.compile('gallery: (.*?),\n', re.S)
    result = re.search(images_pattern, html)
    # 判断是否成功
    if result:
        # 对字符串进行解析，把字符串转化成json对象
        data = json.loads(result.group(1))
        # 判断里面是否含有我们想要的数据
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images_url = [item.get('url') for item in sub_images]
            for image in images_url:
                download_image(image)
            # 返回数据存入数据库
            return {
                'title': title,
                'url': url,
                'images_url': images_url
            }

# 下载图片
def download_image(url):
    print('正在下载', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 因为图片为二进制，所以用content
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片出错',url)
        return None
def save_image(content):
    # 将图片分配md5值，避免重复下载
    file_path = '{0}/{1}.{2}'.format('./toutiao', md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()

# 存入数据库
def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('储存mongodb成功', result)
        return True
    return False

def main(offset):
    html = get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            # 将得到的数据存入数据库
            if result:
                save_to_mongo(result)

if __name__=='__main__':
    groups = [x * 20 for x in range(GROUP_START, GROUP_END + 1)]
    # 多进程加速下载
    pool = Pool()
    pool.map(main, groups)
