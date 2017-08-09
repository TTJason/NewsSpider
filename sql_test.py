# warning this operation is very dangerous ,it will empty the dataset
import pymysql

db = pymysql.connect("localhost", "root", "123456", "news_dataset", charset="utf8")


def execute(sql_file):
    db = pymysql.connect("localhost", "root", "123456", "news_dataset", charset="utf8")
    cursor = db.cursor()
    file = open(sql_file, 'r')
    sql = file.read()
    file.close()
    cursor.execute(sql)
    db.commit()
    db.close()



db.close()


