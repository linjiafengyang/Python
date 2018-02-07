"""
10.4 Pivot Tables and Cross-Tabulation数据透视表和交叉表
"""
# 数据透视表
# 它能按一个或多个keys来把数据聚合为表格，能沿着行或列，根据组键来整理数据
import numpy as np
import pandas as pd
tips = pd.read_csv('tips.csv')
tips['tip_pct'] = tips['tip'] / tips['total_bill']
print(tips.pivot_table(index=['day', 'smoker']))
print(tips.pivot_table(['tip_pct', 'size'], index=['time', 'day'], columns='smoker'))

# 通过设置margins=True来添加部分合计
# 会给行和列各添加All标签，这个All表示的是当前组对于整个数据的统计值
print(tips.pivot_table(['tip_pct', 'size'], index=['time', 'day'], columns='smoker', margins=True))

# 想要使用不同的聚合函数，传递给aggfunc即可
print(tips.pivot_table('tip_pct', index=['time', 'smoker'], columns='day', aggfunc=len, margins=True))

# 如果一些组合是空的（或NA），我们希望直接用fill_value来填充
print(tips.pivot_table('tip_pct', index=['time', 'size', 'smoker'], columns='day', aggfunc='mean', fill_value=0))

"""
1.交叉表
"""
data = pd.DataFrame({'Sample': np.arange(1, 11),
                     'Nationality': ['USA', 'Japan', 'USA', 'Japan', 'Japan', 'Japan', 'USA', 'USA', 'Japan', 'USA'],
                     'Handedness': ['Right-handed', 'Left-handed', 'Right-handed', 'Right-handed', 'Left-handed', 
                     'Right-handed', 'Right-handed', 'Left-handed', 'Right-handed', 'Right-handed']})
print(pd.crosstab(data.Nationality, data.Handedness, margins=True))
# crosstab的前两个参数可以是数组或Series或由数组组成的列表
print(pd.crosstab([tips.time, tips.day], tips.smoker, margins=True))