import csv
from matplotlib import pyplot as plt
from datetime import datetime

# 从文件中获取日期/最高气温
filename = 'C:/Users/linji/Desktop/HW/python/DataVisualization/CSV/sitka_weather_07-2014.csv'

with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    # for index, column_header in enumerate(header_row):
    #     print (index, column_header)
    dates, highs, lows = [], [], []
    differences = []
    for row in reader:
        current_date = datetime.strptime(row[0], "%Y-%m-%d")
        dates.append(current_date)
        # 转成int，让matplotlib能够读取它们
        high = int(row[1])
        highs.append(high)

        low = int(row[3])
        lows.append(low)

        difference = high - low
        differences.append(difference)

# 根据数据绘制图形
fig = plt.figure(dpi=128, figsize=(10, 6))
plt.plot(dates, highs, c='red') # 最高温度
plt.plot(dates, lows, c='blue') # 最低温度
plt.plot(dates, differences, c='green') # 温差

# 设置图形的格式
plt.title("Daily high and low temperatures, July 2014", fontsize=24)
plt.xlabel('', fontsize=16)
# 绘制斜的日期标签，以免它们彼此重叠
fig.autofmt_xdate()
plt.ylabel("Temperature (F)", fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.savefig('C:/Users/linji/Desktop/HW/python/DataVisualization/CSV/sitka_weather_07-2014.png')
plt.show()