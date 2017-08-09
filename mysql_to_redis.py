import pymysql
import redis


def get_name_from_singer():
    data_array = []
    db = pymysql.connect("localhost", "root", "123456", "news_dataset", charset="utf8")
    cursor = db.cursor()
    sql = "select name from singer limit 0,100"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for res, in results:
            print(res)
            data_array.append(results)
    except:
        print("Error: unable to fetch data")
    db.close()
    return data_array


def set_name_to_redis(list):
    pool = redis.ConnectionPool(host='127.0.0.1', port=9212)
    r = redis.Redis(connection_pool=pool)


