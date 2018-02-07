import win_unicode_console
win_unicode_console.enable()
"""
8.2 Combining and Merging Datasets（合并数据集）

pandas里有几种方法可以合并数据：
pandas.merge 按一个或多个key把DataFrame中的行连接起来。
这个和SQL或其他一些关系型数据库中的join操作相似。
pandas.concat 在一个axis（轴）上，串联或堆叠（stack）多个对象。
combine_first 实例方法（instance method）能合并相互之间有重复的数据，
并用一个对象里的值填满缺失值
"""

"""
1.数据库风格的DataFrame Joins
"""
import pandas as pd
import numpy as np

df1 = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
                    'data1': range(7)})
print(df1)
df2 = pd.DataFrame({'key': ['a', 'b', 'd'],
                    'data2': range(3)})
print(df2)
print(pd.merge(df1, df2))
# 如果我们没有指定，merge会用两个对象中都存在的列名作为key（键）
print(pd.merge(df1, df2, on='key'))

# 如果每一个对象中的列名不一样，我们可以分别指定：
df3 = pd.DataFrame({'lkey': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
                    'data1': range(7)})
df4 = pd.DataFrame({'rkey': ['a', 'b', 'd'],
                    'data2': range(3)})
print(pd.merge(df3, df4, left_on='lkey', right_on='rkey'))

# merge默认是inner join(内连接)，结果中的key是交集的结果，或者在两个表格中都有的集合
# outer join（外连接）取key的合集，其实就是left join和right join同时应用的效果：
print(pd.merge(df1, df2, how='outer'))

df1 = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'], 
                    'data1': range(6)})
df2 = pd.DataFrame({'key': ['a', 'b', 'a', 'b', 'd'], 
                    'data2': range(5)})
print(pd.merge(df1, df2, on='key', how='left'))
print(pd.merge(df1, df2, how='inner'))

# 用多个key来连接的话，用一个含有多个列名的list来指定
left = pd.DataFrame({'key1': ['foo', 'foo', 'bar'], 
                     'key2': ['one', 'two', 'one'], 
                     'lval': [1, 2, 3]})

right = pd.DataFrame({'key1': ['foo', 'foo', 'bar', 'bar'], 
                      'key2': ['one', 'one', 'one', 'two'], 
                      'rval': [4, 5, 6, 7]})
print(pd.merge(left, right, on=['key1', 'key2'], how='outer'))
print(pd.merge(left, right, on='key1'))
# merge有一个suffixes选项，能让我们指定字符串，添加重叠的列名到左、右DataFrame：
print(pd.merge(left, right, on='key1', suffixes=('_left', '_right')))


"""
2.在index上做归并
"""
# 可以使用left_index=True 或 right_index=True来指明，哪一个index被用来作为归并键：
left1 = pd.DataFrame({'key': ['a', 'b', 'a', 'a', 'b', 'c'],
                      'value': range(6)})
right1 = pd.DataFrame({'group_val': [3.5, 7]}, index=['a', 'b'])
print(pd.merge(left1, right1, left_on='key', right_index=True))

# merge的默认方法是用key的交集，我们也可以设定用合集，即outer join:
print(pd.merge(left1, right1, left_on='key', right_index=True, how='outer'))

#对于那些有多层级索引的数据，就更复杂了。
# index上的merge默认会是multiple-key merge(复数键归并)：
lefth = pd.DataFrame({'key1': ['Ohio', 'Ohio', 'Ohio',
                               'Nevada', 'Nevada'], 
                      'key2': [2000, 2001, 2002, 2001, 2002], 
                      'data': np.arange(5.)})
righth = pd.DataFrame(np.arange(12).reshape((6, 2)),
                      index=[['Nevada', 'Nevada', 'Ohio', 'Ohio', 
                              'Ohio', 'Ohio'], 
                             [2001, 2000, 2000, 2000, 2001, 2002]], 
                      columns=['event1', 'event2'])
print(pd.merge(lefth, righth, left_on=['key1', 'key2'], right_index=True))
print(pd.merge(lefth, righth, left_on=['key1', 'key2'], right_index=True, how='outer'))

# 同时使用两个对象里的index来归并
left2 = pd.DataFrame([[1., 2.], [3., 4.], [5., 6.]], 
                     index=['a', 'c', 'e'], 
                     columns=['Ohio', 'Nevada'])
right2 = pd.DataFrame([[7., 8.], [9., 10.], [11., 12.], [13, 14]], 
                      index=['b', 'c', 'd', 'e'],
                      columns=['Missouri', 'Alabama'])
print(pd.merge(left2, right2, how='outer', left_index=True, right_index=True))
print(left2.join(right2, how='outer'))

# 最后，对于简单的index-on-index连接，可以直接给join传入一个DataFrame。
another = pd.DataFrame([[7., 8.], [9., 10.], [11., 12.], [16., 17.]], 
                       index=['a', 'c', 'e', 'f'], 
                       columns=['New York', 'Oregon'])
print(left2.join([right2, another]))
print(left2.join([right2, another], how='outer'))


"""
3.沿着轴串联
"""
# Numpy中的concatenate函数可以作用于numpy数组
arr = np.arange(12.).reshape((3, 4))
print(np.concatenate([arr, arr], axis=1))

s1 = pd.Series([0, 1], index=['a', 'b'])
s2 = pd.Series([2, 3, 4], index=['c', 'd', 'e'])
s3 = pd.Series([5, 6], index=['f', 'g'])
print(pd.concat([s1, s2, s3]))

# 默认情况下，concat中axis=0,结果会得到一个新的而series。
# 如果令axis=1, 结果会变成一个DataFrame（axis=1 是列）
print(pd.concat([s1, s2, s3], axis=1))

# 可以通过设定join='inner'来使用交集：
s4 = pd.concat([s1, s3])
print(pd.concat([s1, s4], axis=1, join='inner'))

# 也可以在join_axes中指定使用哪些轴
print(pd.concat([s1, s4], axis=1, join_axes=[['a', 'c', 'b', 'e']]))

# 假设我们想在串联轴上创建一个多层级索引，我们需要用到keys参数：
result = pd.concat([s1, s1, s3], keys=['one', 'two', 'three'])
print(result)
print(result.unstack())

print(pd.concat([s1, s2, s3], axis=1, keys=['one', 'two', 'three']))

df1 = pd.DataFrame(np.arange(6).reshape(3, 2), index=['a', 'b', 'c'], 
                   columns=['one', 'two'])
df2 = pd.DataFrame(5 + np.arange(4).reshape(2, 2), index=['a', 'c'], 
                   columns=['three', 'four'])
print(pd.concat([df1, df2], axis=1, keys=['level1', 'level2']))
print(pd.concat([df1, df2], axis=1, keys=['level1', 'level2'],
          names=['upper', 'lower']))

df1 = pd.DataFrame(np.random.randn(3, 4), columns=['a', 'b', 'c', 'd'])
df2 = pd.DataFrame(np.random.randn(2, 3), columns=['b', 'd', 'a'])
print(pd.concat([df1, df2], ignore_index=True))


"""
4.用重叠来合并数据
"""
a = pd.Series([np.nan, 2.5, np.nan, 3.5, 4.5, np.nan], 
              index=['f', 'e', 'd', 'c', 'b', 'a'])
b = pd.Series(np.arange(len(a), dtype=np.float64), 
              index=['f', 'e', 'd', 'c', 'b', 'a'])
print(np.where(pd.isnull(a), b, a))
print(b[:-2].combine_first(a[2:]))

# 对于DataFrame， combine_first可以在列与列之间做到同样的事情，
# 可以认为是用传递的对象，给调用对象中的缺失值打补丁：
df1 = pd.DataFrame({'a': [1., np.nan, 5., np.nan], 
                    'b': [np.nan, 2., np.nan, 6.], 
                    'c': range(2, 18, 4)})
df2 = pd.DataFrame({'a': [5., 4., np.nan, 3., 7.], 
                    'b': [np.nan, 3., 4., 6., 8.]})
print(df1.combine_first(df2))