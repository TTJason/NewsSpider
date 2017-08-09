import pymysql
import config



db = pymysql.connect(config.host, config.username, config.password, config.database_name, charset="utf8")

def process_lyric(db=db):
    cursor = db.cursor()
    sql = "select lyric from lyric where id = %d" % 479693321
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        result = cursor.fetchone()
        print(result[0])
    except:
        print("Error: unable to fetch data")

process_lyric()
db.close()