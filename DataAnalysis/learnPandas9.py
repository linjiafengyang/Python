import win_unicode_console
win_unicode_console.enable()
"""
7.2 数据转换
"""

"""
1.删除重复值
"""
import pandas as pd
import numpy as np
data = pd.DataFrame({'k1': ['one', 'two'] * 3 + ['two'],
                     'k2': [1, 1, 2, 3, 3, 4, 4]})
# DataFrame方法duplicated返回的是一个boolean Series，
# 表示一个row是否是重复的（根据前一行来判断）
print(data.duplicated())

# drop_duplicateds返回一个DataFrame，会删除重复的部分
print(data.drop_duplicates())

# 上面两种方法都默认考虑所有列
# 我们可以指定一部分来检测重复值。
# 假设我们只想检测'k1'列的重复值
data['v1'] = range(7)
print(data.drop_duplicates(['k1']))

# duplicated和drop_duplicated默认保留第一次观测到的数值组合。
# 设置keep='last'能返回最后一个
print(data.drop_duplicates(['k1', 'k2'], keep='last'))


"""
2.用函数或映射来转换数据
"""
data = pd.DataFrame({'food': ['bacon', 'pulled pork', 'bacon',
                              'Pastrami', 'corned beef', 'Bacon',
                              'pastrami', 'honey ham', 'nova lox'],
                     'ounces': [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})
meat_to_animal = {
    'bacon': 'pig',
    'pulled pork': 'pig',
    'pastrami': 'cow',
    'corned beef': 'cow',
    'honey ham': 'pig',
    'nova lox': 'salmon'
}
# 用于series的map方法接受一个函数，或是一个字典，包含着映射关系，
# 但这里有一个小问题，有些肉是大写，有些是小写。
# 因此，我们先用str.lower把所有的值变为小写:
lowercased = data['food'].str.lower()
# print(lowercased)
data['animal'] = lowercased.map(meat_to_animal)
print(data)

# 我们也可以用一个函数解决上面的问题
print(data['food'].map(lambda x: meat_to_animal[x.lower()]))


"""
3.替换值
"""
data = pd.Series([1., -999., 2., -999., -1000., 3.])
print(data.replace(-999, np.nan))
# 如果想要一次替换多个值，直接用一个list即可
print(data.replace([-999, -1000], np.nan))
# 对于不同的值用不同的替换值，也是导入一个list
print(data.replace([-999, -1000], [np.nan, 0]))
# 参数也可以是一个dict
print(data.replace({-999: np.nan, -1000: 0}))


"""
4.重命名Axis索引
"""
data = pd.DataFrame(np.arange(12).reshape((3, 4)),
                    index=['Ohio', 'Colorado', 'New York'],
                    columns=['one', 'two', 'three', 'four'])
transform = lambda x: x[:4].upper()
print(data.index.map(transform))

# 可以赋值给index，以in-place的方式修改DataFrame
data.index = data.index.map(transform)
print(data)

# 如果你想要创建一个转换后的版本，而且不用修改原始的数据，可以用rename
print(data.rename(index=str.title, columns=str.upper))

# 注意，rename能用于dict一样的oject
print(data.rename(index={'OHIO': 'INDIANA'},
                    columns={'three': 'pekaboo'}))
# 可以用inplace直接修改原始数据
data.rename(index={'OHIO': 'INDIANA'}, inplace=True)
print(data)


"""
5.离散化和装箱
"""
# 假设你有一组数据，你想把人分到不同的年龄组里：
# 我们把这些分到四个bin里，19~25, 26~35, 36~60, >60
# 可以用pandas里的cut
ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
bins = [18, 25, 35, 60, 100]
cats = pd.cut(ages, bins)
print(cats)
# 返回的是一个特殊的Categorical object。
# 我们看到的结果描述了pandas.cut如何得到bins。
# 可以看作是一个string数组用来表示bin的名字，
# 它内部包含了一个categories数组，用来记录不同类别的名字，
# 并伴有表示ages的label（可以通过codes属性查看）：
print(cats.codes)
print(cats.categories)
print(pd.value_counts(cats))

# 也可以用一个list或数组给labels选项来设定bin的名字
group_names = ['Youth', 'YoungAdult', 'MiddleAged', 'Senior']
print(pd.cut(ages, bins, labels=group_names))

# 如果你只是给一个bins的数量来cut，而不是自己设定每个bind的范围，
# cut会根据最大值和最小值来计算等长的bins。
# 比如下面我们想要做一个均匀分布的四个bins
data = np.random.rand(20)
print(pd.cut(data, 4, precision=2))

# qcut，会按照数据的分位数来分箱。取决于数据的分布，
# 用cut通常不能保证每一个bin有一个相同数量的数据点。
# 而qcut是按百分比来切的，所以可以得到等数量的bins：
data = np.random.randn(1000)
cats = pd.qcut(data, 4)
print(pd.value_counts(cats))

# 指定百分比
cats2 = pd.cut(data, [0, 0.1, 0.5, 0.9, 1.])
print(cats2)
print(pd.value_counts(cats2))


"""
6.检测和过滤异常值
"""
data = pd.DataFrame(np.random.randn(1000, 4))
print(data.describe())
# 找一个列中，绝对值大于3的数字
col = data[2] # 第三列
print(col[np.abs(col) > 3])

# 选中所有绝对值大于3的行
print(data[np.abs(data) > 3].head())
# 可以用any方法在一个boolean DataFrame上
print(data[(np.abs(data) > 3).any(1)]) # any中axis=1表示column

# 把绝对值大于3的数字直接变成-3或3
# np.sign(data)会根据值的正负号来得到1或-1
data[np.abs(data) > 3] = np.sign(data) * 3

print(np.sign(data).head())


"""
7.排列和随机采样
"""
df = pd.DataFrame(np.arange(20).reshape((5, 4)))
sampler = np.random.permutation(5)
print(sampler)
print(df.take(sampler))

# 为了选中一个随机的子集，而且没有代替功能
# (既不影响原来的值，返回一个新的series或DataFrame)，
# 可以用sample方法
print(df.sample(n=3))

# 如果想要生成的样本带有替代功能(即允许重复)，
# 给sample中设定replace=True:
choices = pd.Series([5, 7, -1, 6, 4])
draws = choices.sample(n=10, replace=True)
print(draws)


"""
8.计算指示器/虚拟变量
Dummy Variables：虚拟变量，又称虚设变量、名义变量或哑变量,
用以反映质的属性的一个人工变量,是量化了的自变量,通常取值为0或1。
"""
# 如果DataFrame中的一列有k个不同的值，
# 我们可以用一个矩阵或DataFrame用k列来表示，1或0
df = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'],
                    'datal': range(6)})
print(pd.get_dummies(df['key']))

# 如果我们想要给column加一个prefix，
# 可以用data.get_dummies里的prefix参数来实现：
# dummies = pd.get_dummies(df['key'], prefix='key')
# df_with_dummy = df[['data1']].join(dummies)
# print(df_with_dummy)

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('movies.dat', sep='::',
                        header=None, names=mnames, engine='python')
print(movies[:10])

all_genres = []
for x in movies.genres:
    all_genres.extend(x.split('|'))
genres = pd.unique(all_genres)
print(genres)

# 一种构建indicator dataframe的方法是先构建一个全是0的DataFrame
zero_matrix = np.zeros((len(movies), len(genres)))
print(zero_matrix.shape)
dummies = pd.DataFrame(zero_matrix, columns=genres)
print(dummies.head())

# 然后迭代每一部movie，并设置每一行中的dummies为1。
# 使用dummies.columns来计算每一列的genre的指示器：
# gen = movies.genres[0]
# print(gen.split('|'))
# print(dummies.columns.get_indexer(gen.split('|')))
# 然后，使用.iloc，根据索引来设定值
for i, gen in enumerate(movies.genres):
    indices = dummies.columns.get_indexer(gen.split('|'))
    dummies.iloc[i, indices] = 1
print(dummies.head())

# 然后，我们可以结合这个和movies
movies_windic = movies.join(dummies.add_prefix('Genre_'))
print(movies_windic.iloc[0])


np.random.seed(12345)
values = np.random.rand(10)
bins = [0, 0.2, 0.4, 0.6, 0.8, 1.]
print(pd.cut(values, bins))
print(pd.get_dummies(pd.cut(values, bins)))