import pymysql

db = pymysql.connect("localhost", "root", "123456", "news_dataset", charset="utf8")

cursor = db.cursor()

file = open('tencent.sql','r')
sql = file.read()
file.close()
cursor.execute(sql)
db.commit()

db.close()
