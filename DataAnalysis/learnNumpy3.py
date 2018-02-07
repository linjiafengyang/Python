import numpy as np
import matplotlib.pyplot as plt

import win_unicode_console
win_unicode_console.enable()
"""
面向数组编程
"""

"""
主要以[X,Y]=meshgrid(x,y)为例，来对该函数进行介绍。

[X,Y] = meshgrid(x,y) 将向量x和y定义的区域转换成矩阵X和Y,
其中矩阵X的行向量是向量x的简单复制，而矩阵Y的列向量是向量y的简单复制
(注：下面代码中X和Y均是数组，在文中统一称为矩阵了)。

假设x是长度为m的向量，y是长度为n的向量，
则最终生成的矩阵X和Y的维度都是 nm （注意不是mn）
"""
m, n = (5, 3)
x = np.linspace(0, 1, m)
y = np.linspace(0, 1, n)
X, Y = np.meshgrid(x, y)
print(x) # [ 0.  ,  0.25,  0.5 ,  0.75,  1.  ]
print(y) # [ 0. ,  0.5,  1. ]
print(X)
"""
[[ 0.  ,  0.25,  0.5 ,  0.75,  1.  ],
 [ 0.  ,  0.25,  0.5 ,  0.75,  1.  ],
 [ 0.  ,  0.25,  0.5 ,  0.75,  1.  ]]
"""
print(Y)
"""
[[ 0. ,  0. ,  0. ,  0. ,  0. ],
 [ 0.5,  0.5,  0.5,  0.5,  0.5],
 [ 1. ,  1. ,  1. ,  1. ,  1. ]]
"""
# 把X和Y画出来后，就可以看到网格了
# plt.style.use('ggplot')
# plt.plot(X, Y, marker='.', color='blue', linestyle='none')
# plt.show()

# 可以用zip得到网格平面上坐标点的数据
# z = [i for i in zip(X.flat, Y.flat)]
# print(z)

"""
1.像数组操作一样表示条件逻辑：numpy.where
"""
xarr = np.array([1.1, 1.2, 1.3, 1.4, 1.5])
yarr = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
cond = np.array([True, False, True, True, False])
# 列表表达式写法：
result = [(x if c else y) for x, y, c in zip(xarr, yarr, cond)]
print(result)

# np.where写法：
result = np.where(cond, xarr, yarr)
print(result)

# 所有正数变为2，所有负数变为-2
arr = np.random.randn(4, 4)
print(np.where(arr > 0, 2, -2))

# 只把正数变为2，其他不变
print(np.where(arr > 0, 2, arr))

"""
2.数学和统计方法
"""
arr = np.random.randn(5, 4)
print(arr.mean()) # 均值
print(np.mean(arr)) # 均值
print(arr.sum()) # 和
print(np.sum(arr)) # 和
print(arr.mean(axis=1)) # 计算各列之间的平均值
print(arr.sum(axis=0)) # 计算各行总和

arr = np.array([0, 1, 2, 3, 4, 5, 6, 7])
print(arr.cumsum()) # 累加

arr = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
print(arr.cumsum(axis=0)) # 沿着行加法
"""
[[0, 1, 2],
 [3, 5, 7],
 [9, 12, 15]]
"""
print(arr.cumprod(axis=1)) # 沿着列乘法
"""
[[  0,   0,   0],
 [  3,  12,  60],
 [  6,  42, 336]]
"""

"""
3.布尔数组的方法
"""
# sum是用来计算布尔数组中有多少个true的
arr = np.random.randn(100)
print((arr > 0).sum())
# any检测数组中只要有一个ture返回就是true
bools = np.array([False, False, True, False])
print(bools.any())
# all检测数组中都是true才会返回true
print(bools.all())

"""
4.排序
"""
# sort
arr = np.random.randn(6)
arr.sort()
print(arr)

# 多维数组：axis
arr = np.random.randn(5, 3)
arr.sort(1)
print(arr)

"""
5.单一性和其他集合逻辑
"""
# np.unique：返回排好序且不重复的值
names = np.array(['Bob', 'Joe', "Will", 'Bob', 'Will', 'Joe', "Joe"])
print(np.unique(names))

ints = np.array([3, 3, 3, 2, 2, 1, 1, 4, 4])
print(np.unique(ints))

# np.in1d:测试一个数组的值是否在另一个数组里，返回一个布尔数组
values = np.array([6, 0, 0, 3, 2, 5, 6])
print(np.in1d(values, [2, 3, 6]))