"""
Chapter 6
数据加载、存储，文件格式
"""
import win_unicode_console
win_unicode_console.enable()
"""
6.1以文本格式读取和写入数据
"""
import pandas as pd
df = pd.read_csv('ex1.csv')
print(df)
print(pd.read_table('ex1.csv', sep=',')) # read_table指定分隔符

# 一个文件不会总是有header row(页首行)，考虑下面的文件
# 读取这样的文件，设定column name
print(pd.read_csv('ex2.csv', header=None))
print(pd.read_csv('ex2.csv', names=['a', 'b', 'c', 'd', 'message']))

# 如果想要从多列构建一个hierarchical index(阶层型索引)，传入一个包含列名的list
parsed = pd.read_csv('csv_mindex.csv', index_col=['key1', 'key2'])
print(parsed)
"""
		 value1	value2
key1 key2		
one	 a	      1	     2
     b	      3	     4
     c	      5	     6
     d	      7	     8
two	 a	      9	    10
     b	     11	    12
     c	     13	    14
     d	     15	    16
"""

# 在一些情况下，一个table可能没有固定的分隔符，用空格或其他方式来分隔。
# 比如下面这个文件:可以看到区域是通过不同数量的空格来分隔的
# 这种情况下，可以传入一个正则表达式给read_table来代替分隔符。
# 用正则表达式为\s+，我们得到
result = pd.read_table('ex3.txt', sep='\s+')
print(result)

# 我们要跳过第一、三、四行，使用skiprows
print(pd.read_csv('ex4.csv', skiprows=[0, 2, 3]))

# 对于缺失值，pandas使用一些sentinel value(标记值)来代表，比如NA和NULL
result = pd.read_csv('ex5.csv')
print(result)
print(pd.isnull(result))

# na_values选项能把我们传入的字符识别为NA，导入必须是list
result = pd.read_csv('ex5.csv', na_values=['9'])
print(result)

# 我们还可以给不同的column设定不同的缺失值标记符，这样的话需要用到dict
sentinels = {'message': ['foo', 'NA'],
             'something': ['two']}
# 把message列中的foo和NA识别为NA，把something列中的two识别为NA
print(pd.read_csv('ex5.csv', na_values=sentinels))


"""
1.读取一部分文本
"""
# 设置pandas中显示的数量
pd.options.display.max_rows = 10
result = pd.read_csv('ex6.csv', nrows=5)
print(result)

# 读取文件的一部分，可以指定chunksize
# pandas返回的TextParser object能让我们根据chunksize
# 每次迭代文件的一部分。
# 比如，我们想要迭代ex6.csv, 计算key列的值的综合:
chunker = pd.read_csv('ex6.csv', chunksize=1000)
tot = pd.Series([])
for piece in chunker:
    tot = tot.add(piece['key'].value_counts(), fill_value=0)
tot = tot.sort_values(ascending=False)
print(tot[:10])

# TextParser有一个get_chunk方法，能返回任意大小的数据片段
chunker = pd.read_csv('ex6.csv', chunksize=1000)
print(chunker.get_chunk(10))


"""
2.写入数据到文本格式
"""
# 输出为csv格式
data = pd.read_csv('ex5.csv')
data.to_csv('ex5_out.csv')

# 其他一些分隔符也可以使用
# （使用sys.stdout可以直接打印文本，方便查看效果）
import sys
data.to_csv(sys.stdout, sep='|')
# 缺失值会以空字符串打印出来，我们可以自己设定缺失值的指定符
data.to_csv(sys.stdout, na_rep='NULL')
# 如果不指定，行和列会被自动写入。当然也可以设定为不写入
data.to_csv('ex5_out.csv', index=False, header=True)
# 可以指定只读取一部分列，并按你选择的顺序读取
data.to_csv(sys.stdout, index=False, columns=['a', 'b', 'c'])


# series也有一个to_csv方法
import numpy as np
dates = pd.date_range('1/1/2000', periods=7)
ts = pd.Series(np.arange(7), index=dates)
ts.to_csv(sys.stdout)


"""
3.Working with Delimited Formats分隔
"""
# 对于单个字符的分隔符，可以使用python内建的csv方法。
# 只要给csv.reader一个打开的文件即可
import csv
# f = open('ex7.csv')
# reader = csv.reader(f)
# # 迭代这个reader
# for line in reader:
#     print(line)
with open('ex7.csv') as f:
    lines = list(csv.reader(f))
header, values = lines[0], lines[1:]
# 然后我们可以用一个字典表达式来构造一个有列的字典，
# 以及用zip(*values)反转行为列：
data_dict = {h: v for h, v in zip(header, zip(*values))}
print(data_dict)
print(header)
print([x for x in zip(*values)])

# 也可以设定一个分隔符参数给csv.reader
f = open('ex7.csv')
reader = csv.reader(f, delimiter='|')
for line in reader:
    print(line)
f.close()

# 可以用csv.write写入
with open('mydata.csv', 'w') as f:
    writer = csv.writer(f, delimiter=';', lineterminator='\n')
    writer.writerow(('one', 'two', 'three'))
    writer.writerow(('1', '2', '3'))
    writer.writerow(('4', '5', '6'))
    writer.writerow(('7', '8', '9'))


"""
4.JSON Data
"""
obj = """ 
{"name": "Wes", 
 "places_lived": ["United States", "Spain", "Germany"], 
 "pet": null, 
 "siblings": [{"name": "Scott", "age": 30, "pets": ["Zeus", "Zuko"]}, 
              {"name": "Katie", "age": 38, "pets": ["Sixes", "Stache", "Cisco"]}] 
} 
"""
import json
result = json.loads(obj)
# 使用json.dumps，可以把python object转换为JSON
asjson = json.dumps(result)
print(asjson)

# 如何把JSON转变为DataFrame或其他一些结构呢。
# 可以把a list of dicts（JSON object）传给DataFrame constructor
# 而且可以自己指定传入的部分
siblings = pd.DataFrame(result['siblings'], columns=['name', 'age'])
print(siblings)


# pandas.read_json假设JSON数组中的每一个Object，是表格中的一行
data = pd.read_json('example.json')
print(data)
print(data.to_json()) # 输出结果为JSON
print(data.to_json(orient='records'))


"""
5.XML and HTML: Web Scraping
"""
# pandas有一个内建的函数，叫read_html, 这个函数利用lxml
# 和Beautiful Soup这样的包来自动解析HTML，变为DataFrame

# pandas.read_html函数有很多额外选项，
# 但是默认会搜索并试图解析含有<tagble>tag的表格型数据。
# 结果是a list of dataframe
tables = pd.read_html('fdic_failed_bank_list.html')
print(len(tables))
print(tables)

failures = tables[0]
print(failures.head())

# 做一些数据清洗和分析，比如按年计算bank failure的数量
close_timestamps = pd.to_datetime(failures['Closing Date'])
print(close_timestamps.dt.year.value_counts())


# 用lxml解析一个XML格式文件
from lxml import objectify
# 使用lxml.objectify,我们可以解析文件，
# 通过getroot，得到一个指向XML文件中root node的指针：
# path = 'Performance_MNR.xml'
# parsed = objectify.parse(open(path))
# root = parsed.getroot()

# data = []
# skip_fields = ['PARENT_SEQ', 'INDICATOR_SEQ', 'DESIRED_CHANGE', 'DECIMAL_PLACES']
# for elt in root.INDICATOR:
#     el_data = {}
#     for child in elt.getchildren():
#         if child.tag in skip_fields:
#             continue
#         el_data[child.tag] = child.pyval
#     data.append(el_data)
# perf = pd.DataFrame(data)
# print(perf.head())

from io import StringIO
tag = '<a href="http://www.google.com">Google</a>'
root = objectify.parse(StringIO(tag)).getroot()
print(root.get('href'))
print(root.text)