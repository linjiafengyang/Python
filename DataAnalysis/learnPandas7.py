"""
6.4 与数据库的交互
"""
import sqlite3
import pandas as pd
query = """
CREATE TABLE test
(a VARCHAR(20), b VARCHAR(20),
 c REAL,        d INTEGAR
);"""
con = sqlite3.connect('mydata.sqlite')
con.execute(query)
con.commit()

# 插入几行数据
data = [('Atlanta', 'Georgia', 1.25, 6),
        ('Tallahassee', 'Florida', 2.6, 3),
        ('Sacramento', 'California', 1.7, 5)]
stmt = 'INSERT INTO test VALUES(?, ?, ?, ?)'
con.executemany(stmt, data)
con.commit()

cursor = con.execute('select * from test')
rows = cursor.fetchall()
print(rows)
print(cursor.description)
print(pd.DataFrame(rows, columns=[x[0] for x in cursor.description]))

import sqlalchemy as sqla
db = sqla.create_engine('sqlite:///mydata.sqlite')
print(pd.read_sql('select * from test', db))