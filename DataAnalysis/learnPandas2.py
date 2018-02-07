"""
pandas主要功能
"""
import win_unicode_console
win_unicode_console.enable()
"""
1.重新索引
"""
# reindex重新索引
import pandas as pd
obj = pd.Series([4.5, 7.2, -5.3, 3.6], index=['d', 'b', 'a', 'c'])
print(obj)

# 在series上调用reindex能更改index，如果没有对应index的话会引入缺失数据
obj2 = obj.reindex(['a', 'b', 'c', 'd', 'e'])
print(obj2)

obj3 = pd.Series(['blue', 'purple', 'yellow'], index=[0, 2, 4])
print(obj3)
print(obj3.reindex(range(6), method='ffill'))

# 对于DataFrame，reindex能更改row index,或column index
import numpy as np
frame = pd.DataFrame(np.arange(9).reshape(3, 3),
                     index=['a', 'c', 'd'],
                     columns=['Ohio', 'Texas', 'California'])
print(frame)
# 更改行索引
frame2 = frame.reindex(['a', 'b', 'c', 'd'])
print(frame2)
# 更改列索引
states = ['Texas', 'Utah', 'California']
print(frame.reindex(columns=states))
# 还可以使用loc更简洁的reindex
print(frame.loc[['a', 'b', 'c', 'd'], states])


"""
2.按轴删除记录
"""
# 对于series，drop回返回一个新的object，并删去你制定的axis的值
obj = pd.Series(np.arange(5.), index=['a', 'b', 'c', 'd', 'e'])
new_obj = obj.drop('c')
print(new_obj)
print(obj.drop(['d', 'c']))

# 对于DataFrame，index能按行或列的axis来删除
data = pd.DataFrame(np.arange(16).reshape(4, 4),
                    index=['Ohio', 'Colorado', 'Utah', 'New York'],
                    columns=['one', 'two', 'three', 'four'])
# 行处理：如果a sequence of labels(一个标签序列)来调用drop，会删去row labels(axis 0):
print(data.drop(['Colorado', 'Ohio']))
# 列处理：drop列的话，设定axis=1或axis='columns':
print(data.drop('two', axis=1))
print(data.drop(['two', 'four'], axis='columns'))

# drop也可以不返回一个新的object，而是直接更改series or dataframe in-place
obj.drop('c', inplace=True)
print(obj)


"""
3.索引、选择、过滤
"""
obj = pd.Series(np.arange(4.), index=['a', 'b', 'c', 'd'])
print(obj['b'], obj[1])
print(obj[2:4])
print(obj[['b', 'a', 'd']])
print(obj[[1, 3]])
print(obj[obj < 2])

# 用label来slicing(切片)的时候，和python的切片不一样的在于，会包括尾节点
print(obj['b':'c'])
obj['b':'c'] = 5 # 可以直接给选中的label更改值
print(obj)


# 而对于DataFrame，indexing可以通过一个值或序列，选中一个以上的列
data = pd.DataFrame(np.arange(16).reshape((4, 4)),
                    index=['Ohio', 'Colorado', 'Utah', 'New York'],
                    columns=['one', 'two', 'three', 'four'])
print(data['two'])
print(data[['three', 'one']])
print(data[:2])
print(data[data['three'] > 5])
print(data < 5)
data[data < 5] = 0
print(data)

# 用loc和iloc来选择
print(data.loc['Colorado', ['two', 'three']])
"""
two      5
three    6
Name: Colorado, dtype: int64
"""
print(data.iloc[2, [3, 0, 1]])
"""
four    11
one      8
two      9
Name: Utah, dtype: int64
"""
print(data.iloc[2]) # 一行
print(data.iloc[[1, 2], [3, 0, 1]])

# indexing函数也能用于切片，不论是single labels或lists of labels
print(data.loc[:'Utah', 'two'])
print(data.iloc[:, :3][data.three > 5])


"""
4.整数索引
"""
ser = pd.Series(np.arange(3.))
# 使用loc(for label)或ilco(for integers)
print(ser.loc[:1])
print(ser.iloc[:1])

"""
5.算术和数据对齐
"""
s1 = pd.Series([7.3, -2.5, 3.4, 1.5], index=['a', 'c', 'd', 'e'])
s2 = pd.Series([2.1, 3.6, -1.5, 4, 3.1], index=['a', 'c', 'e', 'f', 'g'])
print(s1 + s2)

df1 = pd.DataFrame(np.arange(9.).reshape((3, 3)), columns=list('bcd'),
                    index=['Ohio', 'Texas', 'Colorado'])
df2 = pd.DataFrame(np.arange(12.).reshape(4, 3), columns=list('bde'),
                    index=['Utah', 'Ohio', 'Texas', 'Oregon'])
print(df1 + df2)
# 如果没有相同的列，相减后全是NaN
df1 = pd.DataFrame({'A': [1, 2]})
df2 = pd.DataFrame({'B': [3, 4]})
print(df1 - df2)

# 带填充值的算术方法
df1 = pd.DataFrame(np.arange(12.).reshape((3, 4)),
                    columns=list('abcd'))
df2 = pd.DataFrame(np.arange(20.).reshape((4, 5)),
                    columns=list('abcde'))
df2.loc[1, 'b'] = np.nan
print(df2)
print(df1 + df2) # 不使用填充值的结果
print(df1.add(df2, fill_value=0)) # 使用填充值

# 在reindex（重建索引）的时候，也可以使用fill_value
print(df1.reindex(columns=df2.columns, fill_value=0))


# DataFrame和Series之间的操作
frame = pd.DataFrame(np.arange(12.).reshape((4, 3)),
                     columns=list('bde'),
                     index=['Utah', 'Ohio', 'Texas', 'Oregon'])
series = frame.iloc[0]
print(series)
print(frame - series)

series2 = pd.Series(range(3), index=['b', 'e', 'f'])
print(frame + series2)

# axis参数就是用来匹配轴的。在这个例子里是匹配
# dataframe的row index(axis='index or axis=0)，然后再广播
series3 = frame['d']
print(frame.sub(series3, axis='index'))


"""
6.函数应用和映射
"""
# numpy的ufuncs(element-wise数组方法)也能用在pandas的object上
frame = pd.DataFrame(np.random.randn(4, 3), columns=list('bde'),
                     index=['Utah', 'Ohio', 'Texas', 'Oregon'])
print(np.abs(frame))

# 另一个常用的操作是把一个用在一维数组上的函数，
# 应用在一行或一列上。要用到DataFrame中的apply函数
f = lambda x: x.max() - x.min()
print(frame.apply(f)) # 函数会被用在每一列
print(frame.apply(f, axis='columns')) # 函数会被用在每一行

# 格式化frame中的浮点数
format = lambda x: '%.2f' % x
print(frame.applymap(format))
# applymap的做法是，series有一个map函数，能用来实现element-wise函数
print(frame['e'].map(format))


"""
7.排序
"""
# 按row或column index来排序的话，可以用sort_index方法
obj = pd.Series(range(4), index=['d', 'a', 'b', 'c'])
print(obj.sort_index())

# 在DataFrame，可以用index或其他axis来排序
frame = pd.DataFrame(np.arange(8).reshape((2, 4)),
                     index=['three', 'one'],
                     columns=['d', 'a', 'b', 'c'])
print(frame.sort_index())
print(frame.sort_index(axis=1))
# 默认是升序，可以设置降序
print(frame.sort_index(axis=1, ascending=False))

# 通过值来排序，用sort_values方法
obj = pd.Series([4, 7, -3, 2])
print(obj.sort_values())
# 缺失值会被排在最后
obj = pd.Series([4, np.nan, 7, np.nan, -3, 2])
print(obj.sort_values())

# 对于一个DataFrame，可以用一列或多列作为sort keys。
# 这样的话，只需要把一列或多列的名字导入到sort_values即可
frame = pd.DataFrame({'b': [4, 7, -3, 2], 'a': [0, 1, 0, 1]})
print(frame.sort_values(by='b'))
print(frame.sort_values(by=['a', 'b']))

# rank方法默认会给每个group一个mean rank（平均排名）。
# rank 表示在这个数在原来的Series中排第几名，
# 有相同的数，取其排名平均（默认）作为值
obj = pd.Series([7, -5, 7, 4, 2, 0, 4])
print(obj.sort_values())
# 在obj中，4和4的排名是第4名和第五名，取平均得4.5。
# 7和7的排名分别是第六名和第七名，则其排名取平均得6.5
print(obj.rank())

# rank也可以根据数据被观测到的顺序来设定
# 给第一个看到的7（label 0）设置rank为6，
# 第二个看到的7（label 2）设置rank为7
print(obj.rank(method='first'))

# dataframe 可以根据行或列来计算rank
frame = pd.DataFrame({'b': [4.3, 7, -3, 2],
                        'a': [0, 1, 0, 1],
                        'c': [-2, 5, 8, -2.5]})
print(frame.rank(axis='columns'))


"""
8.有重复label的轴索引
"""
obj = pd.Series(range(5), index=['a', 'a', 'b', 'b', 'c'])
print(obj.index.is_unique)
print(obj['a'])

df = pd.DataFrame(np.random.randn(4, 3), index=['a', 'a', 'b', 'b'])
print(df.loc['b'])