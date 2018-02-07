"""
随机漫步
"""

"""
首先一个最简单的随机漫步：
从0开始，步幅为1和-1，以相同的概率出现。
"""
# 纯python
import random
position = 0
walk = [position]
steps = 1000
for i in range(steps):
    step = 1 if random.randint(0, 1) else -1
    position += step
    walk.append(position)

import matplotlib.pyplot as plt
plt.plot(walk[:100])
plt.show()

# np.random:更快
import numpy as np
nsteps = 1000
draws = np.random.randint(0, 2, size=nsteps)
steps = np.where(draws > 0, 1, -1)
walk = steps.cumsum()
print(walk.min()) # 最小值
print(walk.max()) # 最大值
print((np.abs(walk) >= 10).argmax()) # 返回布尔数组中最大值的索引
# plt.plot(walk[:100])
# plt.show()

"""
一次模拟多个随机漫步
"""
nwalks = 5000
nsteps = 1000
draws = np.random.randint(0, 2, size=(nwalks, nsteps))
steps = np.where(draws > 0, 1, -1)
walks = steps.cumsum(1) # 沿着每行来计算累加
print(walks.max())
print(walks.min())

hits30 = (np.abs(walks) >= 30).any(1)
print(hits30)
print(hits30.sum())