"""
9.2 用pandas和seaborn绘图
"""
"""
1.Line Plots线图
"""
# Series和DataFrame各自都有plot属性，
# 用来做一些比较基本的绘图类型。默认，plot()会绘制线图：
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
# Series对象的index（索引），被matplotlib用来当做x轴，
# 我们也可以自己设定不这么做，use_index=False。
# x轴的ticks（标记）和limits（范围）能通过xticks和xlim选项来设定，
# 而y轴的可以用yticks和ylim来设定
s = pd.Series(np.random.randn(10).cumsum(), index=np.arange(0, 100, 10))
s.plot()
plt.show()

# DataFrame的plot方法，会把每一列画出一条线，
# 所有的线会画在同一个subplot（子图）上，
# 而且可以添加legend（图例）
df = pd.DataFrame(np.random.randn(10, 4).cumsum(0),
                    columns=['A', 'B', 'C', 'D'],
                    index=np.arange(0, 100, 10))
df.plot()
plt.show()


"""
2.Bar Plots条形图
"""
fig, axes = plt.subplots(2, 1)
data = pd.Series(np.random.rand(16), index=list('abcdefghijklmnop'))
# color='k'设置颜色为黑，
# 而alpha=0.7则设置局部透明度（靠近1越明显，靠近0则虚化）
data.plot.bar(ax=axes[0], color='k', alpha=0.7)
data.plot.barh(ax=axes[1], color='k', alpha=0.7)
plt.show()

# 对于DataFrame，条形图绘图会把每一行作为一个组画出来：
df = pd.DataFrame(np.random.rand(6, 4),
                    index=['one', 'two', 'three', 'four', 'five', 'six'],
                    columns=pd.Index(['A', 'B', 'C', 'D'], name='Genus'))
df.plot.bar()
plt.show()

df.plot.bar(stacked=True, alpha=0.5)
plt.show()

df.plot.barh(stacked=True, alpha=0.5)
plt.show()


tips = pd.read_csv('tips.csv')
# print(tips.head())
party_counts = pd.crosstab(tips['day'], tips['size'])
print(party_counts)
# 大于1人小于6人
party_counts = party_counts.loc[:, 2:5]
print(party_counts)
# 标准化一下，让每一行的和变为1，然后绘图
party_pcts = party_counts.div(party_counts.sum(1), axis=0)
party_pcts.plot.bar()
plt.show()

# 试一下用seaborn，按day来查看tipping percentage(小费百分比)
tips['tip_pct'] = tips['tip'] / (tips['total_bill'] - tips['tip'])
sns.barplot(x='tip_pct', y='day', data=tips, orient='h')
plt.show() # 条形图上的黑线表示95%的自信区间（confidence interval）

# seaborn.barplot有一个hue选项，这个能让我们通过一个额外的类别值把数据分开
sns.barplot(x='tip_pct', y='day', hue='time', data=tips, orient='h')
plt.show()


"""
3.Histograms and Density Plots柱状图和密度图
"""
# 柱状图是一种条形图，不过值的频率是分割式的
# 用plot.hist做一个柱状图来表示小费（tip）占总费用（total bill）的比例
tips['tip_pct'].plot.hist(bins=50)
plt.show()

# density plot（密度图），这个是用来计算观测数据中，连续概率分布的推测值
tips['tip_pct'].plot.density()
plt.show()

"""
seaborn能更方便地绘制柱状图和概率图，通过distplot方法，
这个方法可以同时绘制一个柱状图和a continuous density estimate
（一个连续密度估计）。
举个例子，考虑一个bimodal distribution（双峰分布，二项分布），
它由连个不同的标准正态分布组成
"""
comp1 = np.random.normal(0, 1, size=200)
comp2 = np.random.normal(10, 2, size=200)
values = pd.Series(np.concatenate([comp1, comp2]))
sns.distplot(values, bins=100, color='k')
plt.show()


"""
4.Scatter or Point Plots散点图或点图
"""
macro = pd.read_csv('macrodata.csv')
data = macro[['cpi', 'm1', 'tbilrate', 'unemp']]
# 计算log differences（对数差分）
trans_data = np.log(data).diff().dropna()
# 利用seaborn的regplot方法，它可以产生一个散点图并拟合一条回归线
sns.set_style('whitegrid')
sns.regplot('m1', 'unemp', data=trans_data)
plt.show()

# seaborn有一个非常方便的pairplot函数，
# 这个函数可以把每一个参数的柱状图或密度估计画在对角线上
sns.pairplot(trans_data, diag_kind='kde', plot_kws={'alpha': 0.4})
plt.show()


"""
5.Facet Grid and Categorical Data多面网格和类别数据
"""
# seaborn有一个有用的内建函数factorplot，能简化制作各种多面图的过程
sns.factorplot(x='day', y='tip_pct', hue='time', col='smoker', 
                kind='bar', data=tips[tips.tip_pct < 1])
plt.show()

sns.factorplot(x='day', y='tip_pct', row='time', col='smoker', 
                kind='bar', data=tips[tips.tip_pct < 1])
plt.show()

sns.factorplot(x='tip_pct', y='day', kind='box',
               data=tips[tips.tip_pct < 0.5])
plt.show()