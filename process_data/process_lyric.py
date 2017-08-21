# coding = utf-8
import pymysql
import config
import re
from process_data.ltp_model import *
from pypinyin import pinyin, lazy_pinyin
import pypinyin

segmentor = get_segmentor(config.LTP_DATA_DIR)


def process_lyric(text):
    # 执行SQL语句
    # cursor.execute(sql)
    # 获取所有记录列表
    sentence = re.sub(r'[^\u4e00-\u9fa5^\n^\s]', '', text).strip()
    sentence = re.sub(r'([(作词)|(作曲)].*?\n)', '', sentence).strip()
    sentence = re.sub(r'\n(\n)', '', sentence).strip()
    sentence = re.sub(r'，|,', ' ', sentence).strip()
    sentence = re.sub(r'\b( +)\b', ',', sentence).strip()
    sentence = re.sub(r'( +)', '', sentence).strip()
    sentence = re.sub(r'(\n+)', ',', sentence).strip()
    return sentence


def get_pair_rhyme_words(sents):
    # sents = text.split(' ')
    sents = [' '.join(list(segmentor.segment(sent))) for sent in sents]
    # for sent in sents:
    #     print('\\'.join(lazy_pinyin(sent,style=pypinyin.FINALS_TONE3)))
    #     print('\t'.join(sent.split(' ')))


# source为整首词,target为往后延一个词的文本
def process_and_write_to_file(text, source_file, target_file):
    sentence = process_lyric(text)
    if sentence.strip() == '' or len(sentence.strip()) < 20:
        return
    sentence = list(segmentor.segment(sentence))
    sentence.reverse()
    source_sentence = ' '.join(sentence)
    target_sentence = ' '.join(sentence[1:])
    source_sentence = source_sentence.replace('\n', '.').strip()
    target_sentence = target_sentence.replace('\n', '.').strip()

    source_file.write(source_sentence)
    source_file.write('\n')

    target_file.write(target_sentence)
    target_file.write('\n')


# source为韵脚,target为整首词
def process_last_word_and_write_to_file(text, source_file, target_file):
    sentence = process_lyric(text)
    if sentence.strip() == '' or len(sentence.strip()) < 20:
        return
    sentence = list(segmentor.segment(sentence))
    sentence.reverse()
    source_sentence = ' '.join(sentence)
    source_sentence = ' '.join(
        [sent.strip().split(' ')[0] for sent in source_sentence.split(',')
         if len(sent.strip().split(' ')) > 0])
    target_sentence = ' '.join(sentence)
    source_sentence = source_sentence.replace('\n', '.').strip()
    target_sentence = target_sentence.replace('\n', '.').strip()

    source_file.write(source_sentence)
    source_file.write('\n')

    target_file.write(target_sentence)
    target_file.write('\n')

# source为韵脚,target为一句话
def process_word_to_sentence(text, source_file, target_file):
    sentence = process_lyric(text)
    if sentence.strip() == '' or len(sentence.strip()) < 20:
        return
    sentence = list(segmentor.segment(sentence))
    sentence.reverse()
    source_sentence = ' '.join(sentence)
    source_sentence = [sent.strip().split(' ')[0] for sent in source_sentence.split(',') if len(sent.strip().split(' ')) > 0]

    target_sentence = ' '.join(sentence)
    target_sentence = [sent.strip().replace('\n', '') for sent in target_sentence.split(',') if len(sent.strip().split(' ')) > 0]

    assert len(source_sentence) == len(target_sentence)
    source_sentence = '\n'.join(source_sentence)
    target_sentence = '\n'.join(target_sentence)

    source_file.write(source_sentence)
    source_file.write('\n')

    target_file.write(target_sentence)
    target_file.write('\n')



def pure_lyric(text, lyric_file):
    sentence = process_lyric(text)
    if sentence.strip() == '' or len(sentence.strip()) < 30:
        return
    lyric_file.write(sentence.replace('\n',''))
    lyric_file.write('\n')

def write_data_from_db_to_file(source_file_name, target_file_name):
    source_file = open(source_file_name, 'w')
    target_file = open(target_file_name, 'w')
    db = pymysql.connect(config.host, config.username, config.password, config.database_name, charset="utf8")
    cursor = db.cursor()
    sql = "select lyric from lyric where lyric <> '' and lyric <> 'None'"
    print(sql)
    # 执行SQL语句
    cursor.execute(sql)
    result = cursor.fetchall()
    for l, in result:
        # process_last_word_and_write_to_file(l, source_file, target_file)
        process_word_to_sentence(l,source_file,target_file)
        # pure_lyric(l, source_file)
    db.close()

    source_file.close()
    target_file.close()


write_data_from_db_to_file(config.LYRIC_BASE_PATH+'/lyric.source',
                           config.LYRIC_BASE_PATH+'/lyric.target')
