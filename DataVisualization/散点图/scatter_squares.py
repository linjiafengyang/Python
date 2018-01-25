import matplotlib.pyplot as plt
"""使用scatter()绘制散点图并设置其样式"""

#x_values = [1, 2, 3, 4, 5]
#y_values = [1, 4, 9, 16, 25]

# 绘制1-1000的平方散点图
x_values = list(range(1, 1001))
y_values = [x**2 for x in x_values]
# 实参s设置了绘制图形时使用的点的尺寸，c为指定颜色（值越接近于0，指定的颜色越深）
#plt.scatter(x_values, y_values, c=(0, 0, 0.8), edgecolors=None, s=40)
# 颜色映射，下面根据y值设置其颜色：y值较小的点显示为浅蓝色，y值较大的点显示为深蓝色
plt.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues, edgecolors=None, s=40)

# 设置图表标题并给坐标轴加上标签
plt.title("Square Numbers", fontsize=24)
plt.xlabel("Value", fontsize=14)
plt.ylabel("Square of Value", fontsize=14)

# 设置刻度标记的大小
#plt.tick_params(axis='both', which='major', labelsize=14)

# 函数axis()前两个数为x轴的范围，后两个数为y轴的范围
plt.axis([0, 1100, 0, 1100000])

# 自动保存图表，第二个参数表示剪掉多余的空白区域
plt.savefig('./DataVisualization/squares_plot.png', bbox_inches='tight')

plt.show()
