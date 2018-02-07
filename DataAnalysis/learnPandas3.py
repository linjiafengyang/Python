import win_unicode_console
win_unicode_console.enable()
"""
总结和描述性统计
"""
import pandas as pd
import numpy as np

df = pd.DataFrame([[1.4, np.nan], [7.1, -4.5],
                    [np.nan, np.nan], [0.75, -1.3]],
                    index=['a', 'b', 'c', 'd'],
                    columns=['one', 'two'])
print(df)
print(df.sum()) # 使用sum的话，会返回一个series
# 使用axis='columns' or axis=1，计算列之间的和
print(df.sum(axis='columns'))
# 可以用skipna来跳过计算NA
print(df.sum(axis='columns', skipna=False))
print(df.mean(axis='columns', skipna=False))

# idxmin和idxmax，能返回间接的统计值
print(df.idxmax())
# 还能计算累加值
print(df.cumsum())

# describe能一下子产生多维汇总数据
print(df.describe())
# 对于非数值性的数据，describe能产生另一种汇总统计
obj = pd.Series(['a', 'a', 'b', 'c'] * 4)
print(obj.describe())


"""
1.相关性和协方差
"""
price = pd.read_pickle('yahoo_price.pkl')
volume = pd.read_pickle('yahoo_volume.pkl')
print(price.head())
print(volume.head())

# pct_change(): 用来计算同colnums两个相邻的数字之间的变化率
returns = price.pct_change()
print(returns.head())
print(returns.tail())

# corr:协方差
print(returns['MSFT'].corr(returns['IBM']))
print(returns.MSFT.corr(returns.IBM))
# cov:方差
print(returns['MSFT'].cov(returns['IBM']))
print(returns.MSFT.cov(returns.IBM))

# dataframe的corr和cov方法，能返回一个完整的相似性或方差矩阵
print(returns.corr())
print(returns.cov())

# 用Dataframe的corrwith方法，我们可以计算dataframe中不同columns之间，或row之间的相似性。
# 传递一个series:
print(returns.corrwith(returns.IBM))

# 传入一个dataframe能计算匹配的column names质监局的相似性。
# 这里我计算volumn中百分比变化的相似性
print(returns.corrwith(volume))


"""
2.唯一值，值计数
"""
obj = pd.Series(['c', 'a', 'd', 'a', 'a', 'b', 'b', 'c', 'c'])
# unique函数告诉我们series里unique values有哪些
uniques = obj.unique()
print(uniques) # 无序
uniques.sort() # 有序
print(uniques)

# value_counts函数计算series中值出现的频率
# 返回的结果是按降序处理的
print(obj.value_counts())
# vaule_counts也是pandas中的方法
print(pd.value_counts(obj.values, sort=False)) # 不排序

# isin 能实现一个向量化的集合成员关系检查，能用于过滤数据集，
# 检查一个子集，是否在series的values中，或在dataframe的column中
mask = obj.isin(['b', 'c'])
print(mask)
print(obj[mask])

# 与isin相对的另一个方法是Index.get_indexer，能返回一个index array，
# 告诉我们有重复值的values(to_match)，在非重复的values(unique_vals)中对应的索引值
to_match = pd.Series(['c', 'a', 'b', 'b', 'c', 'a'])
unique_vals = pd.Series(['c', 'b', 'a']) # 索引为0/1/2
print(pd.Index(unique_vals).get_indexer(to_match)) # 输出对应的索引

# 计算DataFrame中多个column的柱状图
data = pd.DataFrame({'Qu1': [1, 3, 4, 3, 4],
                     'Qu2': [2, 3, 1, 2, 3],
                     'Qu3': [1, 5, 2, 4, 4]})
result = data.apply(pd.value_counts)
print(result)
"""
	Qu1	Qu2	Qu3
1	1.0	1.0	1.0
2	NaN	2.0	1.0
3	2.0	2.0	NaN
4	2.0	NaN	2.0
5	NaN	NaN	1.0

每一行的laebls(即1，2，3，4，5)其实就是整个data里出现过的值，
从1到5。而对应的每个方框里的值，则是表示该值在当前列中出现的次数。
比如，(2, Qu1)的值是Nan，说明2这个数字没有在Qu1这一列出现过。
(2, Qu2)的值是2，说明2这个数字在Qu2这一列出现过2次。
(2, Qu3)的值是1，说明2这个数字在Qu3这一列出现过1次
"""