import win_unicode_console
win_unicode_console.enable()

import numpy as np
"""
多维数组对象ndarray
"""
# 生成一个两行三列的二维数组
# 数据为随机正态分布数
data = np.random.randn(2, 3)
print(data)
print(data * 10)
print(data.shape) # 维度大小
print(data.dtype) # 数据类型data type

"""
1.创建n维数组
"""
# 使用array函数
data1 = [6, 7.5, 8, 0, 1]
arr1 = np.array(data1)
print(arr1)
# 嵌套序列能被转换为多维数组
data2 = [[1, 2, 3, 4], [5, 6, 7, 8]]
arr2 = np.array(data2)
print(arr2, arr2.ndim, arr2.shape, arr2.dtype) # ndim维度

# zeros函数
# 创建10个0.的一维数组
print(np.zeros(10))
# 创建3行6列的二维数组
print(np.zeros((3, 6)))

# empty函数
# 返回为初始化的垃圾数值
print(np.empty((2, 3, 2)))

# arange函数
# 返回0-14的有序一维数组
print(np.arange(15))

"""
2.dtype保存数据的类型
"""
# 指定dtype
arr1 = np.array([1, 2, 3], dtype=np.float64)
arr2 = np.array([1, 2, 3], dtype=np.int32)
print(arr1.dtype, arr2.dtype)

# 可以用astype来转换数据类型
arr = np.array([1, 2, 3, 4, 5])
float_arr = arr.astype(np.float64) # 转换成float64
print(float_arr.dtype)

arr = np.array([3.7, -1.2, -2.6, 0.5, 12.9, 10.1])
int_arr = arr.astype(np.int32) # 转换成int32
print(int_arr)
print(int_arr.dtype)

# 可以用astype把string里的数字变为实际的数字
# 要十分注意numpy.string_类型，这种类型的长度是固定的，
# 所以可能会直接截取部分输入而不给警告
numeric_strings = np.array(['1.25', '-9.6', '42'], dtype=np.string_)
print(numeric_strings, numeric_strings.dtype)
print(numeric_strings.astype(float)) # 将string转换为float

# 可以用其他数组的dtype直接来指定类型
int_array = np.arange(10)
calibers = np.array([.22, .270, .357, .380, .44, .50], dtype=np.float64)
print(int_array.astype(calibers.dtype)) # int转换为float64

# 可以利用类型的缩写，比如u4代表unit32
empty_unit32 = np.empty(8, dtype='u4')
print(empty_unit32)

"""
3.多维数组计算：同一位置上的元素之间才能进行运算
"""
arr = np.array([[1., 2., 3.], [4., 5., 6.]])
print(arr)
print(arr * arr)
print(1/arr)
print(arr ** 0.5)

# 两个数组的比较会产生布尔数组
arr2 = np.array([[0., 4., 1.], [7., 2., 12.]])
print(arr2 > arr)

"""
4.基本的索引和切片
"""
# 一维数组和list差不多
arr = np.arange(10)
print(arr[5:8])
arr[5:8] = 12 # 第5/6/7个数均变为12
print(arr)

# 在一个二维数组里，单一的索引指代的是一维的数组
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d[2]) # 第三行
print(arr2d[0][2]) # 第一行第三列
print(arr2d[0, 2]) # 第一行第三列

# 对于多维数组，如果省略后面的索引，返回的将是一个低维度的多维数组。
# 比如下面一个2 x 2 x 3数组
arr3d = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
print(arr3d)
print(arr3d[0]) # 返回一个2*3数组

# 标量和数组都能赋给arr3d[0]
old_values = arr3d[0].copy()
arr3d[0] = 42 # 标量
print(arr3d)

arr3d[0] = old_values # 数组
print(arr3d)

# arr3d[1, 0]会给你一个(1, 0)的一维数组
print(arr3d[1, 0])
x = arr3d[1]
print(x[0])

# 二维数组的切片
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d[:2]) # 前两行
print(arr2d[:2, 1:]) # 前两行，第一列之后
print(arr2d[1, :2]) # 第二行的前两列
print(arr2d[:2, 2]) # 前两行的第三列
print(arr2d[:, :1]) # 冒号表示提取整个axis（轴）
arr2d[:2, 1:] = 0 # 前两行，第一列之后赋值为0
print(arr2d)

"""
5.布尔索引
"""
# 用布尔索引总是会返回一份新创建的数据，原本的数据不会被改变。
# 注意：布尔数组和data数组的长度要一样
names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
print(names == 'Bob')
data = np.random.randn(7, 4)
print(data[names == 'Bob'])

# 可以选中names=='Bob'的行，然后索引列
print(data[names == 'Bob', 2:])

# 选中除了'Bob'外的所有行，可以用!=或者~
print(names != 'Bob')
print(data[~(names == 'Bob')])

# 选中2个或3个名字，组合多个布尔条件，用布尔运算符&，|，
# 另外python中的关键词and和or不管用
mask = (names == 'Bob') | (names == 'Will')
print(mask)
print(data[mask])

# 让所有负数变为0
data[data < 0] = 0
print(data)
# 用一维的布尔数组也能更改所有行或列
data[names != 'Joe'] = 7
print(data)

"""
6.花式索引
"""
# 通过整数数组来索引。假设我们有一个8x4的数组
arr = np.empty((8, 4))
for i in range(8):
    arr[i] = i
print(arr)

# 想要按一定顺序选出几行，可以用一个整数list或整数ndarray来指定顺序
print(arr[[4, 3, 0, 6]])
# 用负号来从后选择row
print(arr[[-3, -5, -7]])

# 用多维索引数组，能选出由一维数组中的元素，通过在每个tuple中指定索引
# 8*4数组：从0到31
arr = np.arange(32).reshape((8, 4))
print(arr)
print(arr[[1, 5, 7, 2], [0, 3, 1, 2]]) # 分别对应(1, 0)(5, 3)...

# 先从arr中选出[1, 5, 7, 2]这四行
# 然后[:, [0, 3, 1, 2]]表示选中所有行，但是列的顺序要按0,3,1,2来排
print(arr[[1, 5, 7, 2]][:, [0, 3, 1, 2]])

"""
7.数组转置和轴交换
"""
# 转置也是返回一个view，而不是新建一个数组。
# 有两种方式，一个是transpose方法，一个是T属性
# 3行5列：0-14
arr = np.arange(15).reshape((3, 5))
print(arr)
print(arr.T) # 转置

arr = np.arange(8).reshape((4, 2))
print(arr.T)
print(arr)
print(np.dot(arr.T, arr)) # 计算矩阵乘法的时候，用np.dot

# 对于多维数组，transpose会接受由轴数字组成的tuple，来交换轴
arr = np.arange(16).reshape((2, 2, 4))
print(arr)
"""
array([[[ 0,  1,  2,  3],
        [ 4,  5,  6,  7]],

       [[ 8,  9, 10, 11],
        [12, 13, 14, 15]]])
"""
print(arr.transpose((1, 0, 2)))
"""
array([[[ 0,  1,  2,  3],
        [ 8,  9, 10, 11]],

       [[ 4,  5,  6,  7],
        [12, 13, 14, 15]]])
"""
print(arr.swapaxes(1, 2))
"""
array([[[ 0,  4],
        [ 1,  5],
        [ 2,  6],
        [ 3,  7]],

       [[ 8, 12],
        [ 9, 13],
        [10, 14],
        [11, 15]]])
"""