import numpy as np

"""
通过数组来进行文件的输入和输出
"""
# np.save和np.load
# 数组会以未压缩的原始二进制模式被保存，后缀为.npy
arr = np.arange(10)
np.save('./some_array', arr)
print(np.load('./some_array.npy'))

# 用np.savez能保存多个数组，还可以指定数组对应的关键字，
# 不过是未压缩的npz格式
np.savez('./array_archive.npz', a=arr, b=arr)
# 加载.npz文件的时候，得到一个dict object
arch = np.load('./array_archive.npz')
print(arch['b'])

# 可以用np.savez_compressed来压缩文件
np.savez_compressed('./array_compressed.npz', a=arr, b=arr)