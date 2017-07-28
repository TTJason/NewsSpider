import pymysql

db = pymysql.connect("localhost", "root", "123456", "news_dataset", charset="utf8")

cursor = db.cursor()
sql = "DROP TABLE IF EXISTS tencent;" \
      "CREATE TABLE `tencent` (\
  `title` varchar(128) NOT NULL,\
  `content` varchar(20000) NOT NULL,\
  `date` varchar(64) NOT NULL,\
  `id` varchar(64) NOT NULL,\
  `cname` varchar(64) NOT NULL,\
  `url` varchar(128) NOT NULL\
) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
sql1 = "DROP TABLE tencent;"
cursor.execute(sql)
db.commit()

db.close()
