import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# data = np.arange(10)
# plt.plot(data)
# plt.show()

"""
1.图和子图
"""
# 在matplotlib中画的图，都是在Figure对象中的。
# 可以用plt.figure创建一个
fig = plt.figure()
# 我们不能在一个空白的figure上绘图，
# 必须要创建一个或更多的subplots（子图），用add_subplot:
# figure是2x2（这样一共有4幅图），
# 而且我们选中4个subplots（数字从1到4）中的第1个
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)

# matplotlib会把图画在最后一个figure的最后一个子图上
#'k--'是一个style（样式）选项，它表示使用黑色的虚线
plt.plot(np.random.randn(50).cumsum(), 'k--') # ax3
ax1.hist(np.random.randn(100), bins=20, color='k', alpha=0.3)
ax2.scatter(np.arange(30),np.arange(30) + 3 * np.random.randn(30))
plt.show()

# plt.subplots方法创建一个新的figure，
# 并返回一个numpy数组，其中包含创建的subplot对象：
f, axes = plt.subplots(2, 3)
plt.show()
# print(axes)

# 用Figure对象下的subplots_adjust方法来更改间隔，当然，也可以用第一层级的函数
# wspace和hspace控制figure宽度和长度的百分比，可以用来控制subplot之间的间隔
fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)
for i in range(2):
    for j in range(2):
        axes[i, j].hist(np.random.randn(500), bins=50, color='k', alpha=0.5)
plt.subplots_adjust(wspace=0, hspace=0)
plt.show()


"""
2.颜色，标记，线条样式
"""
# 字符串必须按颜色，标记物类型，样式这样的顺序
# plt.plot(np.random.randn(30).cumsum(), 'ko--') # is also ok
plt.plot(np.random.randn(30).cumsum(), color='k', linestyle='dashed', marker='o')
plt.show()

# 我们把label传递给了plot，这样通过plt.legend显示出每条线的意义。
data = np.random.randn(30).cumsum()
plt.plot(data, 'k--', label='Default')
plt.plot(data, 'k-', drawstyle='steps-post', label='steps-post')
plt.legend(loc='best')
plt.show()


"""
3.标记，标签，图例
"""
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(np.random.randn(1000).cumsum(), 'k', label='one')
ax.plot(np.random.randn(1000).cumsum(), 'k--', label='two')
ax.plot(np.random.randn(1000).cumsum(), 'k.', label='three')
ax.legend(loc='best')
# 为了改变x-axis tick（x轴标记），使用set_xticks和set_xticklabels。
# 前者告诉matplotlib沿着x轴的范围，把标记放在哪里；
# 默认会把所在位置作为标签，但我们可以用set_xticklabels来设置任意值作为标签：
ticks = ax.set_xticks([0, 250, 500, 750, 1000])
labels = ax.set_xticklabels(['one', 'two', 'three', 'four', 'five'],
                             rotation=30, fontsize='small')
ax.set_title('My first matplotlib plot')
ax.set_xlabel('Stages')
# axes类有一个set方法，能让我们一次设置很多绘图特性。
# 对于上面的例子，我们可以写成下面这样
# props = {
#     'title': 'My first matplotlib plot',
#     'xlabel': 'Stages'
# }
# ax.set(**props)

plt.show()


"""
4.注释和在subplot上画图
"""
from datetime import datetime
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
data = pd.read_csv('spx.csv', index_col=0, parse_dates=True)
spx = data['SPX']
spx.plot(ax=ax, style='k-')
crisis_data = [
    (datetime(2007, 10, 11), 'Peak of bull market'),
    (datetime(2008, 3, 12), 'Bear Stearns Fails'),
    (datetime(2008, 9, 15), 'Lehman Bankruptcy')
]
# ax.annotate方法能在x和y坐标指示的位置画出标签
for date, label in crisis_data:
    ax.annotate(label, xy=(date, spx.asof(date) + 75),
                xytext=(date, spx.asof(date) + 225),
                arrowprops=dict(facecolor='black', headwidth=4, width=2, headlength=4),
                horizontalalignment='left', verticalalignment='top')
# 设置范围边界
ax.set_xlim(['1/1/2007', '1/1/2011'])
ax.set_ylim([600, 1800])
ax.set_title('Important dates in the 2008-2009 financial crisis')
plt.show()


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
rect = plt.Rectangle((0.2, 0.75), 0.4, 0.15, color='k', alpha=0.3)
circ = plt.Circle((0.7, 0.2), 0.15, color='b', alpha=0.3)
pgon = plt.Polygon([[0.15, 0.15], [0.35, 0.4], [0.2, 0.6]], color='g', alpha=0.5)
ax.add_patch(rect)
ax.add_patch(circ)
ax.add_patch(pgon)
plt.show()


"""
5.保存图片plt.savefig
# dpi，控制每英寸长度上的分辨率
#bbox_inches, 能删除figure周围的空白部分
"""
"""
6.matplotlib设置
"""
# 设置全局的图大小为10 x 10
# plt.rc('figure', figsize=(10, 10))
# rc中的第一个参数是我们想要自定义的组件，
# 比如'figure', 'axes', 'xtick', 'ytick', 'grid', 'legend'，或其他。
# 然后添加一个关键字来设定新的参数。
# 一个比较方便的写法是把所有的设定写成一个dict：
# font_options = {'family': 'monospace',
#                 'weight': 'bold',
#                 'size'  : 'small'}
# plt.rc('font', **font_options)