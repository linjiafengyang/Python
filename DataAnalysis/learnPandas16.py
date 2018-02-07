import win_unicode_console
win_unicode_console.enable()
"""
10.3 应用：通用的分割-应用-合并
"""
import numpy as np
import pandas as pd
tips = pd.read_csv('tips.csv')
tips['tip_pct'] = tips['tip'] / tips['total_bill']
print(tips.head())

def top(df, n=5, column='tip_pct'):
    return df.sort_values(by=column)[-n:]
print(top(tips, n=6))

# 按smoker分组，然后用apply来使用这个函数
print(tips.groupby('smoker').apply(top))

print(tips.groupby(['smoker', 'day']).apply(top, n=1, column='total_bill'))

result = tips.groupby('smoker')['tip_pct'].describe()
print(result)
print(result.unstack('smoker'))


"""
1.Suppressing the Group Keys抑制组键
"""
# 多层级索引是由原来的对象中，组键（group key）在每一部分的索引上得到的。
# 我们可以在groupby函数中设置group_keys=False来关闭这个功能
print(tips.groupby('smoker', group_keys=False).apply(top))

"""
2.Quantile and Bucket Analysis分位数与桶分析
"""
frame = pd.DataFrame({'data1': np.random.randn(1000), 'data2': np.random.randn(1000)})
quartiles = pd.cut(frame.data1, 4)
print(quartiles[:10])

def get_stats(group):
    return {'min': group.min(), 'max': group.max(),
            'count': group.count(), 'mean': group.mean()}
grouped = frame.data2.groupby(quartiles)
print(grouped.apply(get_stats).unstack())

# 把frame的data1列分为10个bin，每个bin都有相同的数量。
# 因为一共有1000个样本，所以每个bin里有100个样本。
# grouping保存的是每个样本的index以及其对应的bin的编号。
grouping = pd.qcut(frame.data1, 10, labels=False)
print(grouped.apply(get_stats).unstack())

"""
3.例子：用组特异性值来填充缺失值
"""
s = pd.Series(np.random.randn(6))
s[::2] = np.nan
print(s)
print(s.fillna(s.mean()))

states = ['Ohio', 'New York', 'Vermont', 'Florida',
            'Oregon', 'Nevada', 'California', 'Idaho']
group_key = ['East'] * 4 + ['West'] * 4
print(group_key)
data = pd.Series(np.random.randn(8), index=states)
print(data)
# 令data中某些值为缺失值
data[['Vermont', 'Nevada', 'Idaho']] = np.nan
print(data.groupby(group_key).mean())
fill_mean = lambda g: g.fillna(g.mean())
print(data.groupby(group_key).apply(fill_mean))

# 我们可能希望提前设定好用于不同组的填充值。
# 因为group有一个name属性，我们可以利用这个
fill_values = {'East': 0.5, 'West': -1}
fill_func = lambda g: g.fillna(fill_values[g.name])
print(data.groupby(group_key).apply(fill_func))


"""
4.例子：随机抽样和排列
"""
# Hearts红桃，Spades黑桃，Clubs梅花，Diamonds方片
suits = ['H', 'S', 'C', 'D']
card_val = (list(range(1, 11)) + [10] * 3) * 4
base_names = ['A'] + list(range(2, 11)) + ['J', 'K', 'Q']
cards = []
for suit in suits:
    cards.extend(str(num) + suit for num in base_names)
deck = pd.Series(card_val, index=cards)
print(deck[:13])
# 随机从牌组中抽出5张牌
def draw(deck, n=5):
    return deck.sample(n)
print(draw(deck))

# 从每副花色中随机抽取两张，花色是每张牌名字的最后一个字符
# （即H, S, C, D），我们可以根据花色分组，然后使用apply
get_suit = lambda card: card[-1] # 花色是每张牌名字的最后一个字符
print(deck.groupby(get_suit).apply(draw, n=2))
print(deck.groupby(get_suit, group_keys=False).apply(draw, n=2))


"""
5.例子：组加权平均和相关性
"""
df = pd.DataFrame({'category': ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b'],
                    'data': np.random.randn(8),
                    'weights': np.random.rand(8)})
print(df)
# 按category分组来计算组加权平均
grouped = df.groupby('category')
get_wavg = lambda g: np.average(g['data'], weights=g['weights'])
print(grouped.apply(get_wavg))


close_px = pd.read_csv('stock_px_2.csv', parse_dates=True, index_col=0)
print(close_px.info())
print(close_px[-4:])

spx_corr = lambda x: x.corrwith(x['SPX'])
rets = close_px.pct_change().dropna()
get_year = lambda x: x.year
by_year = rets.groupby(get_year)
print(by_year.apply(spx_corr))
print(by_year.apply(lambda g: g['AAPL'].corr(g['MSFT'])))


"""
6.例子：组对组的线性回归
"""
# 我们可以定义regress函数（利用statsmodels库），
# 在每一个数据块（each chunk of data）上进行普通最小平方回归
# （ordinary least squares (OLS) regression）计算
import statsmodels.api as sm
def regress(data, yvar, xvars):
    Y = data[yvar]
    X = data[xvars]
    X['intercept'] = 1
    result = sm.OLS(Y, X).fit()
    return result.params
print(by_year.apply(regress, 'AAPL', ['SPX']))
