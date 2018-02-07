"""
6.3 Web API
"""
import pandas as pd
import numpy as np
import requests
url = 'https://api.github.com/repos/pandas-dev/pandas/issues'
resp = requests.get(url)
data = resp.json()
# print(data[0]['title'])
# print(data[0])
issues = pd.DataFrame(data, columns=['number', 'title', 'labels', 'created_at'])
# print(issues)

import xlrd
import openpyxl
issues.to_excel('issues.xlsx')
issues.to_csv('issues.csv', index=False)
