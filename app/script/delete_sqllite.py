import sqlite3

# 连接到SQLite数据库
conn = sqlite3.connect('../../db.sqlite3')
cursor = conn.cursor()

# 查询所有用户创建的表名，排除sqlite_sequence表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
tables = cursor.fetchall()

# 构造并执行删除每个表的SQL语句
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")

# 提交更改并关闭连接
conn.commit()
conn.close()
