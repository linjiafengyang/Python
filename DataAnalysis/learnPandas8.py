import win_unicode_console
win_unicode_console.enable()
"""
7.1 处理缺失数据
"""
import pandas as pd
import numpy as np
string_data = pd.Series(['aardvark', 'artichoke', np.nan, 'avocado'])
print(string_data.isnull())

"""
1.过滤缺失值
"""
# 可以使用pandas.isnull和boolean indexing, 配合使用dropna。
# 对于series，只会返回non-null数据和index values
from numpy import nan as NA
data = pd.Series([1, NA, 3.5, NA, 7])
print(data.dropna())
print(data[data.notnull()])

# 对于DataFrame，可能想要删除包含有NA的row和column。
# dropna默认会删除包含有缺失值的row
data = pd.DataFrame([[1., 6.5, 3.], [1., NA, NA],
                    [NA, NA, NA], [NA, 6.5, 3.]])
print(data.dropna())
# 设定how=all只会删除那些全是NA的行
print(data.dropna(how='all'))

# 删除列也一样，设置axis=1
data[4] = NA
print(data.dropna(axis=1, how='all'))

# 假设你想要保留有特定数字的观测结果，可以使用thresh参数：
df = pd.DataFrame(np.random.randn(7, 3))
df.iloc[:4, 1] = NA
df.iloc[:2, 2] = NA
print(df.dropna())
print(df.dropna(thresh=2))


"""
2.填补缺失值
"""
# 调用fillna的时候设置好一个常用用来替换缺失值
print(df.fillna(0))
# 给fillna传入一个dict，可以给不同列替换不同的值
print(df.fillna({1: 0.5, 2: 0}))
# fillna返回一个新对象，但你可以使用in-place来直接更改原有的数据
df.fillna(0, inplace=True)
print(df)

# 在使用fillna的时候，这种插入法同样能用于reindexing
df = pd.DataFrame(np.random.randn(6, 3))
df.iloc[2:, 1] = NA
df.iloc[4:, 2] = NA
print(df.fillna(method='ffill'))
print(df.fillna(method='ffill', limit=2))

# 使用fillna可以我们做一些颇有创造力的事情。
# 比如，可以传入一个series的平均值或中位数
data = pd.Series([1., NA, 3.5, NA, 7])
print(data.fillna(data.mean()))
