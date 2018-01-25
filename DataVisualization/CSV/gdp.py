import csv
from matplotlib import pyplot as plt
from datetime import datetime

# 从文件中获取日期/最高气温/最低气温
filename = 'C:/Users/linji/Desktop/HW/python/DataVisualization/CSV/gdp.csv'

with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    # for index, column_header in enumerate(header_row):
    #     print (index, column_header)
    dates, gdps_chn, gdps_usa = [], [], []
    for row in reader:
        try:
            date = int(row[2])
            # 转成int，让matplotlib能够读取它们
            if row[1] == 'CHN':
                gdp_chn = float(row[3])
            else:
                gdp_usa = float(row[3])
        except ValueError:
            print (date, 'missing data')
        else:
            if date not in dates:
                dates.append(date)
            if row[1] == 'CHN':
                gdps_chn.append(gdp_chn)
            else:
                gdps_usa.append(gdp_usa)

# 根据数据绘制图形
fig = plt.figure(dpi=128, figsize=(10, 6))
plt.plot(dates, gdps_chn, c='red', alpha=0.5)
plt.plot(dates, gdps_usa, c='blue', alpha=0.5)


# 设置图形的格式
plt.title("The GDP of China and USA From 1960 To 2016", fontsize=20)
plt.xlabel('Year', fontsize=16)
plt.ylabel("GDP", fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.savefig('C:/Users/linji/Desktop/HW/python/DataVisualization/CSV/gdp.png')
plt.show()