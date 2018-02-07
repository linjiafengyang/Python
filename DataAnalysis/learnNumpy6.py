import numpy as np
"""
伪随机数生成
"""
# 之所以称之为伪随机数，是因为随机数生成算法是根据seed来生成的。
# 也就是说，只要seed设置一样，每次生成的随机数是相同的
np.random.seed(1234)
samples = np.random.normal(size=(4, 4))
print(samples)

# 当然，这个seed是全局的，如果想要避免全局状态，
# 可以用numpy.random.RandomState来创建一个独立的生成器
rng = np.random.RandomState(1234)
print(rng.randn(10))
