from gensim.models import Word2Vec
from gensim.models import word2vec
import numpy as np
import config

def train(filename, modelname,vocab_path,embedding_path):
    sents = word2vec.Text8Corpus(filename)
    model = Word2Vec(sents, size=128, window=5, min_count=5, workers=4)
    model.save(modelname)
    write_vocab(model, vocab_path)
    write_vocab_embedding(model, embedding_path)


def write_vocab(model, path):
    file = open(path, 'w')
    file.write('\n'.join(model.wv.index2word[:30000]))
    file.close()


def write_vocab_embedding(model, path):
    embedding_array = []
    for i in model.wv.index2word:
        embedding_array.append(model.wv.word_vec(i))
    embedding_array = np.array(embedding_array)
    np.save(path, embedding_array)


train(config.LYRIC_BASE_PATH+'/lyric.target',
      config.LYRIC_BASE_PATH+'/w2v.model',
      config.LYRIC_BASE_PATH+'/vocab',
      config.LYRIC_BASE_PATH+'/embedding')
