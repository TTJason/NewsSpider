# -*- coding: utf-8 -*-

import os
import pyltp
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser
from pyltp import SementicRoleLabeller


# 分词
def get_segmentor(LTP_DATA_DIR):
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
    segmentor = Segmentor()  # 初始化实例
    segmentor.load(cws_model_path)  # 加载模型
    return segmentor


# 词性标注
def get_postagger(LTP_DATA_DIR):
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
    postagger = Postagger()  # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    return postagger


# 实体标注
def get_recognizer(LTP_DATA_DIR):
    ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
    recognizer = NamedEntityRecognizer()  # 初始化实例
    recognizer.load(ner_model_path)  # 加载模型
    return recognizer


# 句法分析
def get_parser(LTP_DATA_DIR):
    par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
    parser = Parser()  # 初始化实例
    parser.load(par_model_path)  # 加载模型
    return parser


# 语义角色标注
def get_labeller(LTP_DATA_DIR):
    srl_model_path = os.path.join(LTP_DATA_DIR, 'srl')  # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
    labeller = SementicRoleLabeller()  # 初始化实例
    labeller.load(srl_model_path)  # 加载模型
    return labeller


class LTPModel(object):
    def __init__(self,
                 text,
                 segmentor,
                 postagger,
                 recognizer,
                 parser,
                 labeller):
        assert len(text) > 0
        self.text = text
        self.seg_words = None
        self.postags = None
        self.netags = None
        self.arcs = None
        self.roles = None

        if segmentor is not None:
            self.segment(segmentor)
        if postagger is not None:
            self.postag(postagger)
        if recognizer is not None:
            self.recognize(recognizer)
        if parser is not None:
            self.parse(parser)
        if labeller is not None:
            self.label(labeller)

    # 分词
    def segment(self, model):
        if self.seg_words is None:
            assert isinstance(model, Segmentor)
            self.seg_words = list(model.segment(self.text))
        print("\t".join(self.seg_words))
        return self.seg_words

    # 词性标注
    def postag(self, model):
        if self.postags is None:
            assert isinstance(model, Postagger)
            self.postags = list(model.postag(self.seg_words))
        print("\t".join(self.postags))
        return self.postags

    # 命名实体识别
    def recognize(self, model):
        if self.netags is None:
            assert isinstance(model, NamedEntityRecognizer)
            self.netags = list(model.recognize(self.seg_words, self.postags))
        print("\t".join(self.netags))
        return self.netags

    # 句法分析
    def parse(self, model):
        if self.arcs is None:
            assert isinstance(model, Parser)
            self.arcs = model.parse(self.seg_words, self.postags)
        print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in self.arcs))
        return self.arcs

    # 语义角色
    def label(self, model):
        if self.roles is None:
            assert isinstance(model, SementicRoleLabeller)
            self.roles = model.label(self.seg_words,
                                     self.postags,
                                     self.netags,
                                     self.arcs)  # 语义角色标注
        for role in self.roles:
            print(role.index, "".join(
                ["%s:(%d,%d)" %
                 (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
        return self.roles
