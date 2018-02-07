"""
6.2 Binary Data Formats (二进制数据格式)
"""
"""
最简单的以二进制的格式来存储数据的方法
（也被叫做serialization，序列化），
就是用python内建的pickle。

所有的pandas object都有一个to_pickle方法，
可以用来存储数据为pickle格式：
"""
import pandas as pd
import numpy as np
frame = pd.read_csv('ex1.csv')
frame.to_pickle('frame_pickle')

# 用内建的pickle可以直接读取任何pickle文件，
# 或者直接用pandas.read_pickle
print(pd.read_pickle('frame_pickle'))
"""
注意：pickle只推荐用于短期存储。因为这种格式无法保证长期稳定；
比如今天pickled的一个文件，可能在库文件更新后无法读取。
"""


"""
1.Using HDF5 Format
HDF5格式是用来存储大量的科学数组数据的
HDF表示hierarchical data forma

HDF5对于处理大数据集是一个很好的选择，
因为他不会把所有数据一次性读取到内存里，
我们可以从很大的数组中有效率地读取一小部分
"""
# import h5py
# import tables
# frame = pd.DataFrame({'a': np.random.randn(100)})
# store = pd.HDFStore('mydata.h5')
# store['obj1'] = frame
# store['obj1_col'] = frame['a']

# # HDFStore支持两种存储架构，fixed和table。
# # 后者通常更慢一些，但支持查询操作
# store.put('obj2', frame, format='table')
# print(store.select('obj2', where=['index >= 10 and index <= 15']))

# frame.to_hdf('../examples/mydata.h5', 'obj3', format='table')
# pd.read_hdf('../examples/mydata.h5', 'obj3', where=['index < 5'])


"""
2.读取Excel文件
"""
import xlrd
import openpyxl
# 读取Excel文件
xlsx = pd.ExcelFile('ex1.xlsx')
print(pd.read_excel(xlsx, 'Sheet1'))
frame = pd.read_excel('ex1.xlsx', 'Sheet1')

# 把pandas数据写为Excel文件
# 先创建一个ExcelWrite，然后用to_excel方法
writer = pd.ExcelWriter('ex2.xlsx')
frame.to_excel(writer, 'Sheet1')
writer.save()

# 如果不用ExcelWriter的话，可以直接传给to_excel一个path
frame.to_excel('ex2.xlsx')