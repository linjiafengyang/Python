"""
7.3 操纵字符串
"""
"""
1.字符串对象方法
Python内建的string方法
"""
val = 'a,b, guido'
print(val.split(','))
# split经常和strip一起搭配使用来去除空格（包括换行符）
pieces = [x.strip() for x in val.split(',')]
print(pieces)

first, second, third = pieces
print(first + '::' + second + '::' + third)
print('::'.join(pieces)) # 更python的方法使用join

#注意index和find的区别。
# 如果要找的string不存在的话，index会报错。而find会返回-1:
print('guido' in val)
print(val.index(','))
print(val.find(':'))

# count会返回一个substring出现的次数
print(val.count(','))
# replace替换指定字符
print(val.replace(',', ''))


"""
2.正则表达式
"""
import re
# re模块有以下三个类别：
# patther matching模式匹配, substitution替换, splitting分割

text = "foo    bar\t baz  \tqux"
print(re.split('\s+', text))

# 可以自己编译regex，
# 用re.compile，可以生成一个可以多次使用的regex object：
regex = re.compile('\s+')
print(regex.split(text))

# 使用findall方法可以得到符合regex的所有结果，结果以list返回
print(regex.findall(text))


text = """Dave dave@google.com 
          Steve steve@gmail.com 
          Rob rob@gmail.com 
          Ryan ryan@yahoo.com """
pattern = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'
regex = re.compile(pattern, flags=re.IGNORECASE)
print(regex.findall(text))
# search返回text中的第一个匹配结果
m = regex.search(text)
print(m)
print(text[m.start():m.end()])
print(regex.match(text)) # None

# sub替换
print(regex.sub('READCTED', text))

# 假设你想要找到邮件地址，同时，想要把邮件地址分为三个部分，
# username, domain name, and domain suffix.（用户名，域名，域名后缀）。
# 需要给每一个pattern加一个括号：
pattern = r'([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})'
regex = re.compile(pattern, flags=re.IGNORECASE)
m = regex.match('wesm@bright.net')
print(m.groups()) # groups方法返回一个tuple

print(regex.findall(text)) # findall会返回a list of tuples

#sub也能访问groups的结果，不过要使用特殊符号 \1, \2。
# \1表示第一个匹配的group，\2表示第二个匹配的group，以此类推
print(regex.sub(r'Username: \1, Domain: \2, Suffix: \3', text))

"""
3.pandas中的字符串向量化函数
"""
import numpy as np
import pandas as pd
data = {'Dave': 'dave@google.com', 'Steve': 'steve@gmail.com',
        'Rob': 'rob@gmail.com', 'Wes': np.nan}
data = pd.Series(data)
print(data)
print(data.str.findall(pattern, flags=re.IGNORECASE))
