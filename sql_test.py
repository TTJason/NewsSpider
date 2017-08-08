# warning this operation is very dangerous ,it will empty the dataset
import pymysql

def create_singer_and_lyric():
    db = pymysql.connect("localhost", "root", "123456", "news_dataset", charset="utf8")

    cursor = db.cursor()

    file = open('songs.sql','r')
    sql = file.read()
    file.close()
    cursor.execute(sql)
    db.commit()

    db.close()
