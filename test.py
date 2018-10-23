#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-06 17:42:05
# @Author  : guangqiang_xu (981886190@qq.com)
# @Version : $Id$

from textrank4zh import TextRank4Keyword, TextRank4Sentence
from news_classifier.news_classifier import triple_classifier
from get_news_type import get_news_label

en2ch = {
    'politics': u'政治',
    'diplomacy': u'外交',
    'economic': u'经济',
    'violence': u'暴恐',
    'coup': u'政变',
    'other': u'其他',
}

# 第一种提取关键词和类别
def news_type_keyword(title,summary):
    '''
    :param title: 新闻标题 
    :param summary: 新闻摘要或者内容
    :return: 关键词，类别
    '''
    n_gram = 2
    w_text = title.encode('utf-8', 'ignore') + \
             summary.encode('utf-8', 'ignore')
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=w_text, lower=True, window=n_gram)
    k_dict = tr4w.get_keywords(500, word_min_len=2)
    keywords = []
    for word in k_dict:
        keywords.append(word["word"])
    keywords_string = (' ').join(keywords)
    keyword = keywords_string
    text = title.encode('utf-8', 'ignore') + \
           summary.encode('utf-8', 'ignore')
    if len(text):
        label = triple_classifier(text)
    else:
        label = 'other'
    new_laber = en2ch[label]

    return keyword,new_laber

# 第二种提取类别
def news_type(content):
    '''
    :param content: 新闻内容 
    : label.txt 文件内自定义关键词类别，
    '''
    get_news_label(content)