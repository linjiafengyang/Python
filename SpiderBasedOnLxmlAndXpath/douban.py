# coding:utf-8
import requests
from lxml import html

n = 1
for i in range(10):
    url = 'https://movie.douban.com/top250?start={}&filter='.format(i * 25)
    r = requests.get(url).content
    # 调用lxml库和html.fromstring函数来解析html
    sel = html.fromstring(r)

    # 影片信息都在class属性为info的div标签里，可以先把这个节点取出来
    for i in sel.xpath('//div[@class="info"]'):
        # 影片名称
        title = i.xpath('div[@class="hd"]/a/span[@class="title"]/text()')[0]

        info = i.xpath('div[@class="bd"]/p[1]/text()')
        # 导演演员信息
        info_director_and_actor = info[0].replace(" ", "").replace("\n", "")
        # 上映日期
        info_date = info[1].replace(" ", "").replace("\n", "").split("/")[0]
        # 制片国家
        info_country = info[1].replace(" ", "").replace("\n", "").split("/")[1]
        # 影片类型
        info_type = info[1].replace(" ", "").replace("\n", "").split("/")[2]
        # 评分
        rate = i.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]
        # 评论人数
        rate_number = i.xpath('div[@class="bd"]/div[@class="star"]/span[4]/text()')[0]

        # 写入文件
        with open("豆瓣电影Top250.txt", "a", encoding='utf-8') as f:
            f.write("TOP%s\n影片名称：%s\n评分：%s %s\n上映日期：%s\n上映国家：%s\n%s\n" % (n, title, rate, rate_number, info_date, info_country, info_director_and_actor))
            f.write("\n====================================\n\n")
        
        n += 1
