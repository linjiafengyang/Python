import win_unicode_console
win_unicode_console.enable()

import pandas as pd
from pandas import Series, DataFrame
import numpy as np
"""
pandas的数据结构:Series和DataFrame
"""

"""
1.Series
series是一个像数组一样的一维序列，
并伴有一个数组表示label，叫做index
"""
obj = pd.Series([4, 7, -5, 3])
print(obj)
print(obj.index)
print(obj.values)

# 可以自己指定index的label
obj2 = pd.Series([4, 7, -5, 3], index=['d', 'b', 'a', 'c'])
print(obj2)
print(obj2.index)
# 可以用index的label来选择
print(obj2['a'])
obj2['d'] = 6
print(obj2[['c', 'a', 'd']])
print(obj2[obj2 > 0])
print(obj2 * 2)

# 另一种看待series的方法，它是一个长度固定，有顺序的dict，
# 从index映射到value。在很多场景下，可以当做dict来用
print('b' in obj2)
print('e' in obj2)

# 还可以直接用现有的dict来创建series
sdata = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
obj3 = pd.Series(sdata)
print(obj3)

# series中的index其实就是dict中排好序的keys。我们也可以传入一个自己想要的顺序
states = ['California', 'Ohio', 'Oregon', 'Texas']
obj4 = pd.Series(sdata, index=states)
print(obj4)

# pandas中的isnull和notnull函数可以用来检测缺失数据
print(pd.isnull(obj4))
print(pd.notnull(obj4))
print(obj4.isnull())

# 数据对齐
print(obj3 + obj4)

# series自身和它的index都有一个叫name的属性
# 能和其他pandas的函数进行整合
obj4.name = 'population'
obj4.index.name = 'state'
print(obj4)

# series的index能被直接更改
obj.index = ['Bob', 'Steve', 'Jeff', 'Ryan']
print(obj)


"""
2.DataFrame
"""
# 构建一个dataframe的方法，用一个dcit，dict里的值是list
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002, 2003],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
frame = pd.DataFrame(data)
print(frame)

# 用head方法会返回前5行（注：这个函数在数据分析中经常使用，用来查看表格里有什么东西）
print(frame.head())

# 如果指定一列的话，会自动按列排序
print(pd.DataFrame(data, columns=['year', 'state', 'pop']))
# 如果你导入一个不存在的列名，那么会显示为缺失数据NaN
frame2 = pd.DataFrame(data, columns=['year', 'state', 'pop', 'debt'],
    index=['one', 'two', 'three', 'four', 'five', 'six'])
print(frame2)
print(frame2.columns)
print(frame2.index)

# 从DataFrame里提取一列的话会返回series格式，
# 可以以属性或是dict一样的形式来提取
print(frame2['state']) # frame2[column]能应对任何列名
print(frame2.state) # 但frame2.column的情况下，列名必须是有效的python变量名才行

# 对于行，要用在loc属性里用 位置或名字
print(frame2.loc['three'])

# 列值也能通过赋值改变
frame2['debt'] = 16.5
print(frame2)

# 如果把list或array赋给column的话，长度必须符合DataFrame的长度。
# 如果把一二series赋给DataFrame，会按DataFrame的index来赋值，
# 不够的地方用缺失数据来表示
val = pd.Series([-1.2, -1.5, -1.7], index=['two', 'four', 'five'])
frame2['debt'] = val
print(frame2)

# 如果列不存在，赋值会创建一个新列
frame2['eastern'] = frame2.state == 'Ohio'
print(frame2)
# del也能像删除字典关键字一样，删除列
del frame2['eastern']
print(frame2)


# 另一种常见的格式是dict中的dict
# 这种嵌套dict传给DataFrame，
# pandas会把外层dcit的key当做列，内层key当做行索引
pop = {'Nevada': {2001: 2.4, 2002: 2.9},
        'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
frame3 = pd.DataFrame(pop)
print(frame3)
"""
	 Nevada	Ohio
2000	NaN	1.5
2001	2.4	1.7
2002	2.9	3.6
"""

# DataFrame也可以像numpy数组一样做转置
print(frame3.T)

# 指定index
print(pd.DataFrame(pop, index=[2001, 2002, 2003]))

# 如果DataFrame的index和column有自己的name属性，也会被显示
frame3.index.name = 'year'
frame3.columns.name = 'state'
print(frame3)
# values属性会返回二维数组
print(frame3.values)


"""
3.索引对象
"""
# index object是不可更改的
obj = pd.Series(range(3), index=['a', 'b', 'c'])
index = obj.index
print(index)

labels = pd.Index(np.arange(3))
print(labels)
obj2 = pd.Series([1.5, -2.5, 0], index=labels)
print(obj2)