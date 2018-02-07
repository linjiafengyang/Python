import win_unicode_console
win_unicode_console.enable()
"""
第10章 数据汇总和组操作
"""
"""
10.1 分组机制
"""
import numpy as np
import pandas as pd
df = pd.DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'],
                    'key2': ['one', 'two', 'one', 'two', 'one'],
                    'data1': np.random.randn(5),
                    'data2': np.random.randn(5)})
# 通过使用key1作为labels，来计算data1列的平均值
grouped = df['data1'].groupby(df['key1'])
print(grouped.mean())

# 用了两个key来分组，得到的结果series现在有一个多层级索引，
# 这个多层索引是根据key1和key2不同的值来构建的
means = df['data1'].groupby([df['key1'], df['key2']]).mean()
print(means)
print(means.unstack())

states = np.array(['Ohio', 'California', 'California', 'Ohio', 'Ohio'])
years = np.array([2005, 2005, 2006, 2005, 2006])
print(df['data1'].groupby([states, years]).mean())

print(df.groupby('key1').mean())
print(df.groupby(['key1', 'key2']).mean())


"""
1.对组进行迭代
"""
for name, group in df.groupby('key1'):
    print(name)
    print(group)
for (k1, k2), group in df.groupby(['key1', 'key2']):
    print((k1, k2))
    print(group)

pieces = dict(list(df.groupby('key1')))
print(pieces)
print(pieces['b'])

grouped = df.groupby(df.dtypes, axis=1)
for dtype, group in grouped:
    print(dtype)
    print(group)

"""
2.选中一列或列的子集
"""
# 只计算data2列的平均值，并将结果返还为一个DataFrame
print(df.groupby(['key1', 'key2'])[['data2']].mean())


"""
3.用Dicts与Series进行分组
"""
people = pd.DataFrame(np.random.randn(5, 5), columns=['a', 'b', 'c', 'd', 'e'],
                        index=['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
people.iloc[2:3, [1, 2]] = np.nan
mapping = {'a': 'red', 'b': 'red', 'c': 'blue', 'd': 'blue', 'e': 'red', 'f': 'orange'}
by_column = people.groupby(mapping, axis=1)
print(by_column.sum())

map_series = pd.Series(mapping)
print(map_series)
print(people.groupby(map_series, axis=1).count())


"""
4.用函数进行分组
"""
# len函数在每一个index（即名字）上被调用了
print(people.groupby(len).sum())

key_list = ['one', 'one', 'one', 'two', 'two']
print(people.groupby([len, key_list]).min())


"""
5.按索引层级来分组
"""
columns = pd.MultiIndex.from_arrays([['US', 'US', 'US', 'JP', 'JP'], 
                                     [1, 3, 5, 1, 3]], 
                                    names=['cty', 'tenor'])
hier_df = pd.DataFrame(np.random.randn(4, 5), columns=columns)
print(hier_df)
# 按层级分组，传入层级的数字或者名字，通过使用level关键字
print(hier_df.groupby(level='cty', axis=1).count())