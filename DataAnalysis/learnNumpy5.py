import numpy as np
"""
线性代数
"""
x = np.array([[1., 2., 3.], [4., 5., 6.]])
y = np.array([[6., 23.], [-1, 7], [8, 9]])
print(x.dot(y)) # 矩阵相乘
print(np.dot(x, y))

# x中的每一行与[1, 1, 1]点对点乘积后求和
print(np.dot(x, np.ones(3)))
print(x @ np.ones(3))

"""
np.linalg能用来做矩阵分解，以及比如转置和求秩之类的事情
"""
from numpy.linalg import inv, qr
X = np.random.randn(5, 5)
print(X)
# # 用np.round控制小数点后的位数
# X = np.round(np.random.randn(5, 5), 3)
# print(X)
mat = X.T.dot(X) # X和X的转置的矩阵乘法
print(np.round(mat, 2))

print(np.round(inv(mat), 2))

print(np.round(mat.dot(inv(mat)), 2))

q, r = qr(mat)
print(np.round(r, 2))