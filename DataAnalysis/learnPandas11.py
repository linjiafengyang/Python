import win_unicode_console
win_unicode_console.enable()
"""
8.1 分层索引
"""
import pandas as pd
import numpy as np
data = pd.Series(np.random.randn(9),
                 index=[['a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'd'],
                        [1, 2, 3, 1, 3, 1, 2, 2, 3]])
print(data)
print(data.index)
print(data['b'])
print(data['b':'c'])
print(data.loc[['b', 'd']])
print(data.loc[:, 2])

# 可以用unstack来把数据进行重新排列，产生一个DataFrame：
print(data.unstack())
# 相反的操作是stack:
print(data.unstack().stack())

# 对于dataframe，任何一个axis(轴)都可以有一个分层索引：
frame = pd.DataFrame(np.arange(12).reshape((4, 3)),
                     index=[['a', 'a', 'b', 'b'], [1, 2, 1, 2]],
                     columns=[['Ohio', 'Ohio', 'Colorado'],
                              ['Green', 'Red', 'Green']])
print(frame)

# 每一层级都可以有一个名字（字符串或任何python对象）
frame.index.names = ['key1', 'key2']
frame.columns.names = ['state', 'color']
print(frame)

# 选中部分列
print(frame['Ohio'])

# MultiIndex能被同名函数创建，而且可以重复被使用；
# 在DataFrame中给列创建层级名可以通过以下方式：
print(pd.MultiIndex.from_arrays([['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']],
                                names=['state', 'color']))

"""
1.重排序和层级排序
"""
# swaplevel会取两个层级编号或者名字，并返回一个层级改变后的新对象（数据本身并不会被改变）
print(frame.swaplevel('key1', 'key2'))

# sort_index则是在一个层级上，按数值进行排序
print(frame.sort_index(level=1))
print(frame.sort_index(level='key2'))

# 把key1与key2交换后，按key2来排序
print(frame.swaplevel(0, 1).sort_index(level=0))


"""
2.按层级来归纳统计数据
"""
print(frame.sum(level='key2'))
print(frame.sum(level='color', axis=1))


"""
3.利用DataFrame的列来索引
"""
frame = pd.DataFrame({'a': range(7), 'b': range(7, 0, -1),
                      'c': ['one', 'one', 'one', 'two', 'two',
                            'two', 'two'],
                      'd': [0, 1, 2, 0, 1, 2, 3]})
print(frame)

# DataFrame的set_index会把列作为索引，并创建一个新的DataFrame
frame2 = frame.set_index(['c', 'd'])
print(frame2)
# 默认删除原先的列，当然我们也可以留着
print(frame.set_index(['c', 'd'], drop=False))

# reset_index的功能与set_index相反，它会把多层级索引变为列
print(frame2.reset_index())