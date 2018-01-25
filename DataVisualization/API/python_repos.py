import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

import win_unicode_console
win_unicode_console.enable()

# 执行API调用并存储响应
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
r = requests.get(url)
print ('Status code: ', r.status_code)

# 将API响应存储在一个变量中
response_dict = r.json()
print ('Total repositories: ', response_dict['total_count'])

# 探索有关仓库的信息
repo_dicts = response_dict['items']
# print ('\nRepositories returned: ', len(repo_dicts))
# for repo_dict in repo_dicts:
#     print (repo_dict['name'])
names, stars = [], []

# 研究第一个仓库
# repo_dict = repo_dicts[0]
# print ('\nKeys: ', len(repo_dict))
# for key in sorted(repo_dict.keys()):
#     print (key)
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])
    stars.append(repo_dict['stargazers_count'])

# 可视化
my_style = LS('#333366', base_style=LCS)
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24 # 图表标题
my_config.label_font_size = 14 # 副标签
my_config.major_label_font_size = 18 # 主标签
my_config.truncate_label = 15 # 将较长的项目名缩短为15个字符
my_config.show_y_guides = False # 隐藏图表中的水平线
my_config.width = 1000 # 自定义宽度，充分利用浏览器可用空间
chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Most-Starred Python Projects on Github'
chart.x_labels = names # 横坐标显示

chart.add('', stars) # 纵坐标显示
chart.render_to_file('C:/Users/linji/Desktop/HW/python/DataVisualization/API/python_repos.svg')