# warning this operation is very dangerous ,it will empty the dataset
import pymysql
import config
db = pymysql.connect(config.host, config.username, config.password, config.database_name, charset="utf8")


def execute(sql_file):
    db = pymysql.connect(config.host, config.username, config.password, config.database_name, charset="utf8")
    cursor = db.cursor()
    file = open(sql_file, 'r')
    sql = file.read()
    file.close()
    cursor.execute(sql)
    db.commit()
    db.close()

execute('songs.sql')
execute('lyric.sql')

db.close()


