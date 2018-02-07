import numpy as np
"""
通用函数
"""
# 一元通用函数
arr = np.arange(10)
print(np.sqrt(arr)) # 平方根，没有改变原有的arr
print(np.exp(arr)) # 指数，没有改变原有的arr

# 二元通用函数
x = np.random.randn(8)
y = np.random.randn(8)
print(np.maximum(x, y)) # 点对点比较x和y中的元素

arr = np.random.randn(7) * 5
print(arr)
remainder, whole_part = np.modf(arr) # modf会返回小数部分和整数部分
print(remainder)
print(whole_part)

print(np.sqrt(arr, arr)) # 改变原有的arr