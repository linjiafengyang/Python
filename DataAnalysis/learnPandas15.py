import win_unicode_console
win_unicode_console.enable()
"""
10.2 Data Aggregation数据聚合
"""
import numpy as np
import pandas as pd
df = pd.DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'],
                    'key2': ['one', 'two', 'one', 'two', 'one'],
                    'data1': np.random.randn(5),
                    'data2': np.random.randn(5)})
grouped = df.groupby('key1')
for key, group in grouped:
    print(key)
    print(group)

print(grouped['data1'].quantile(0.9))

# 如果想用自己设计的聚合函数，把用于聚合数组的函数传入到aggregate或agg方法即可：
def peak_to_peak(arr):
    return arr.max() - arr.min()
print(grouped.agg(peak_to_peak))

print(grouped.describe())


"""
1.列对列和多函数应用
"""
tips = pd.read_csv('tips.csv')
tips['tip_pct'] = tips['tip'] / tips['total_bill']
print(tips[:6])

grouped = tips.groupby(['day', 'smoker'])
grouped_pct = grouped['tip_pct']
for name, group in grouped_pct:
    print(name)
    print(group[:2], '\n')
print(grouped_pct.agg('mean'))

# 如果我们把函数或函数的名字作为一个list传入，
# 我们会得到一个DataFrame，每列的名字就是函数的名字
print(grouped_pct.agg(['mean', 'std', peak_to_peak]))

# 上面结果的列名是自动给出的，当然，
# 我们也可以更改这些列名。这种情况下，
# 传入一个由tuple组成的list，每个tuple的格式是(name, function)，每
# 个元组的第一个元素会被用于作为DataFrame的列名
# （我们可以认为这个二元元组list是一个有序的映射）
print(grouped_pct.agg([('foo', 'mean'), ('bar', np.std)]))

functions = ['count', 'mean', 'max']
result = grouped['tip_pct', 'total_bill'].agg(functions)
print(result)
print(result['tip_pct'])

ftuples = [('Durchschnitt', 'mean'), ('Abweichung', np.var)]
print(grouped['tip_pct', 'total_bill'].agg(ftuples))
print(grouped.agg({'tip': np.max, 'size': sum}))
print(grouped.agg({'tip_pct': ['min', 'max', 'mean', 'std'], 'size': 'sum'}))


"""
2.不使用行索引返回聚合数据
"""
print(tips.groupby(['day', 'smoker'], as_index=False).mean())
