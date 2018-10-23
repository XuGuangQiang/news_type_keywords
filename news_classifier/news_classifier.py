# -*- coding: utf-8 -*-

import re
#import opencc
import os
import time
import csv
import json
from gensim import corpora
from utils import load_scws, cut
result_path = './result/'

AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'classify_dict')

cut_str = load_scws()

dictionary_3 = corpora.Dictionary.load(os.path.join(AB_PATH, 'new_classify.dict'))
step3_score = {}
with open(os.path.join(AB_PATH, 'new_classify.txt')) as f:
    for l in f:
        lis = l.rstrip().split()
        step3_score[int(lis[0])] = [float(lis[1]), float(lis[2]), float(lis[3]), float(lis[4]), float(lis[5])]


def triple_classifier(text):

    entries = cut(cut_str, text)
    entry = [e.decode('utf-8', 'ignore') for e in entries]
    keywords_list = entry
        
        
    bow = dictionary_3.doc2bow(entry)
    s = [1, 1, 1, 1, 1]
    for pair in bow:
        s[0] = s[0] * (step3_score[pair[0]][0] ** pair[1])
        s[1] = s[1] * (step3_score[pair[0]][1] ** pair[1])
        s[2] = s[2] * (step3_score[pair[0]][2] ** pair[1])
        s[3] = s[3] * (step3_score[pair[0]][3] ** pair[1])
        s[4] = s[4] * (step3_score[pair[0]][4] ** pair[1])

    s_max = max(s)
    s_dis = abs(s[0]-s_max) + abs(s[1]-s_max) + abs(s[2]-s_max) + abs(s[3]-s_max) + abs(s[4]-s_max)
    if (s_dis/5)/s_max <= 0.7:
        label = 'other'
    else:
        
        if s[0] > s[1] and s[0] > s[2] and s[0] > s[3] and s[0] > s[4]:#政治领域
            label = 'politics'
        elif s[1] > s[0] and s[1] > s[2] and s[1] > s[3] and s[1] > s[4]:#外交领域
            label = 'diplomacy'
        elif s[2] > s[0] and s[2] > s[1] and s[2] > s[3] and s[2] > s[4]:#经济领域
            label = 'economic'
        elif s[3] > s[0] and s[3] > s[1] and s[3] > s[2] and s[3] > s[4]:#暴恐领域
            label = 'violence'
        elif s[4] > s[0] and s[4] > s[1] and s[4] > s[3] and s[4] > s[2]:#政变领域
            label = 'coup'
        else:
            label = 'other'

    return label

def get_file_data(_id):
    
    f = open(result_path + 'recommend_news_%s.jl' % _id)
    news_data = []
    for line in f:
        news_dict = json.loads(line)
        news_data.append(news_dict)

    return news_data

def write_file_data(_id,result):

    f = open(result_path + 'classify_result_%s.jl' % _id,'a')
    
    for item in result:
        row = json.dumps(item)
        f.write(row+'\n')

    f.close()

if __name__ == '__main__':

    news_data = get_file_data('1487665506')
    result = []
    for news in news_data:
        if news.has_key('title') and news.has_key('summary'):
            text = news['title'].encode('utf-8','ignore') + news['summary'].encode('utf-8','ignore')
        elif news.has_key('title') and not news.has_key('summary'):
            text = news['title'].encode('utf-8','ignore')
        elif not news.has_key('title') and news.has_key('summary'):
            text = news['summary'].encode('utf-8','ignore')
        else:
            text = ''

        if len(text):#非空字符
            label = triple_classifier(text)
        else:
            label = 'other'
        news['label'] = label
        result.append(news)

    write_file_data('1487665506',result)


    
