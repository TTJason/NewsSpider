import pymysql
import config
import re


def write_data_from_db_to_file(file_name):
    source_file = open(file_name, 'w')
    db = pymysql.connect(config.host, config.username, config.password, config.database_name, charset="utf8")
    cursor = db.cursor()
    sql = "select title from tencent where title <> '' and cname='要闻'"
    print(sql)
    # 执行SQL语句
    cursor.execute(sql)
    result = cursor.fetchall()
    for l, in result:
        title = re.sub(r'GIF-', '', l).strip()
        if '：' in title:
            title = title.split('：')[1]
        if ':' in title:
            title = title.split(':')[1]
        source_file.write(title)
        source_file.write('\n')
    db.close()

    source_file.close()
write_data_from_db_to_file(config.TITLE_PATH)