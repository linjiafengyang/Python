import win_unicode_console
win_unicode_console.enable()

"""
8.3 Reshaping and Pivoting
"""

"""
1.对多层级索引进行reshape
"""
import numpy as np
import pandas as pd

data = pd.DataFrame(np.arange(6).reshape((2, 3)),
                    index=pd.Index(['Ohio', 'Colorado'], name='state'),
                    columns=pd.Index(['one', 'two', 'three'], name='number'))
print(data)

# 使用stack方法会把列数据变为行数据，产生一个Series
result = data.stack()
print(result)
# 对于一个有多层级索引的Series，可以用unstack把它变回DataFrame
print(result.unstack())
# 默认会把最内层的层级unstack（取消堆叠），stack默认也是这样。
# 我们可以传入一个表示层级的数字或名字，来指定取消堆叠某个层级：
print(result.unstack(0))
print(result.unstack('state'))

# 如果某个层级里的值不能在subgroup(子组)里找到的话，unstack可能会引入缺失值
s1 = pd.Series([0, 1, 2, 3], index=['a', 'b', 'c', 'd'])
s2 = pd.Series([4, 5, 6], index=['c', 'd', 'e'])
data2 = pd.concat([s1, s2], keys=['one', 'two'])
print(data2)
print(data2.unstack())
print(data2.unstack().stack()) #stack默认会把缺失值过滤掉
print(data2.unstack().stack(dropna=False))

# 如果对一个DataFrame使用unstack，被取消堆叠（unstack）的层级会变为结果中最低的层级
df = pd.DataFrame({'left': result, 'right': result + 5},
                    columns=pd.Index(['left', 'right'], name='side'))
print(df)
print(df.unstack('state')) # state被unstack后，变为比side更低的层级
# 调用stack的时候，可以指明想要stack（堆叠）哪一个轴
print(df.unstack('state').stack('side'))


"""
2.把长格式旋转为宽格式
"""
data = pd.read_csv('macrodata.csv')
print(data.head())

periods = pd.PeriodIndex(year=data.year, quarter=data.quarter, name='date')
columns = pd.Index(['realgdp', 'inf1', 'unemp'], name='item')
data = data.reindex(columns=columns)
data.index = periods.to_timestamp('D', 'end')
ldata = data.stack().reset_index().rename(columns={0: 'value'})
print(ldata[:10])

pivoted = ldata.pivot('date', 'item', 'value')
print(pivoted)


"""
3.把宽格式旋转为长格式
"""
# 与pivot相反的操作是pandas.melt
df = pd.DataFrame({'key': ['foo', 'bar', 'baz'],
                    'A': [1, 2, 3],
                    'B': [4, 5, 6],
                    'C': [7, 8, 9]})
print(df)
# 'key'列可以作为group indicator（群指示器），其他列可以作为数据值。
# 当使用pandas.melt，我们必须指明哪些列是群指示器。这里我们令key作为群指示器：
melted = pd.melt(df, ['key'])
print(melted)

# 使用pivot，我们可以得到原来的布局
reshaped = melted.pivot('key', 'variable', 'value')
print(reshaped)
# 因为pivot会给行标签创建一个索引（key列），所以这里我们要用reset_index来让数据变回去
print(reshaped.reset_index())

# 我们也可以在使用melt的时候指定哪些列用于值：
print(pd.melt(df, id_vars=['key'], value_vars=['A', 'B']))

# pandas.melt也能在没有群指示器的情况下使用
print(pd.melt(df, value_vars=['A', 'B', 'C']))
print(pd.melt(df, value_vars=['key', 'A', 'B']))
