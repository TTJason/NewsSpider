import pymysql
import config
import re

db = pymysql.connect(config.host, config.username, config.password, config.database_name, charset="utf8")


def process_lyric(db=db):
    cursor = db.cursor()
    sql = "select lyric from lyric where id = %s" % 229779
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        result = cursor.fetchone()
        sentences = re.sub(r'[^\u4e00-\u9fa5^\n^\s]', '', result[0]).strip()
        sentences = re.sub(r'([(作词)|(作曲)].*?\n)', '', sentences).strip()
        sentences = re.sub(r'\n(\n)', '', sentences).strip()
        sentences = re.sub(r'\b( +)', ',', sentences).strip()
        sentences = sentences.split('\n')
        for sent in sentences:
            print(sent)
    except:
        print("Error: unable to fetch data")


print(re.sub(r'\b( +)', ',', ' 作词  庄奴').strip())
process_lyric()
db.close()
