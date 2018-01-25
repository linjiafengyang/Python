import matplotlib.pyplot as plt

from random_walk import RandomWalk
"""将随机漫步的所有点绘制出来"""

# 只要程序处于活动状态，就不断地模拟随机漫步
while True:
    # 创建一个RandomWalk实例，并将其包含的点都绘制出来
    rw = RandomWalk(50000)
    rw.fill_walk()

    # 设置绘图窗口和尺寸
    plt.figure(dpi=128, figsize=(10, 6))
    # 给点着色，颜色映射
    point_numbers = list(range(rw.num_points))
    #plt.plot(rw.x_values, rw.y_values, linewidth=1)
    plt.scatter(rw.x_values, rw.y_values, c=point_numbers, cmap=plt.cm.Blues, edgecolors=None, s=1)

    # 突出起点和终点
    #plt.scatter(0, 0, c='green', edgecolors=None, s=100)
    #plt.scatter(rw.x_values[-1], rw.y_values[-1], c='red', edgecolors=None, s=100)
    #plt.scatter(rw.x_values, rw.y_values, s=15)
    plt.show()

    keep_running = input("Make another walk? (y/n): ")
    if keep_running == 'n':
        break
