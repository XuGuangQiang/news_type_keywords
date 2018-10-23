# -*- coding: utf-8 -*-

#  gathering snmp data
from __future__ import division
import os
import sys
import datetime
import random
import time
import re
import scws
import csv
from gensim import corpora, models, similarities
import math
import string
from utils import single_word_whitelist,black_word,load_scws,cx_dict

sw = load_scws()

def read_csv(d_time):

    text_list = []
    word_dict = dict() 
    files = os.listdir('./%s/' % d_time)
    for filename in files:
        f = open('./%s/%s' % (d_time,filename))
        count = 0
        text = ''
        for line in f:
            count = count + 1
            print count
            line = line.decode('gbk', 'ignore')
            line = line.encode('utf-8')
            w_text = line.strip('\n\t\r')
            w_text = w_text.replace(' ','')
            
            text = text + w_text
        f.close()
        text_list.append(text)

    return text_list

def read_csv_2(d_time):

    reader = csv.reader(file('./%s_ori.csv' % d_time, 'rb'))
    text_list = []
    for title,text in reader:
        text_list.append(title+'。'+text)

    return text_list

def main_two(p_text,n_text):#暴恐、政变
  
    dictionary_p = corpora.Dictionary([])
    print len(p_text),len(n_text)

    for p in p_text:
        kw_pos = sw.participle(p)
        entries = []
        for kw in kw_pos:
            if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
                entries.append(kw[0])
        dictionary_p.add_documents([entries])

    for n in n_text:
        kw_pos = sw.participle(n)
        entries = []
        for kw in kw_pos:
            if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
                entries.append(kw[0])
        dictionary_p.add_documents([entries])

    dictionary_p.filter_extremes(10,0.7,1000000)
    dictionary_p.compactify()
    dictionary_p.save('./classify_dict/second_classify.dict')

    kw_count = dict()
    kw_score = dict()
    for kw in range(len(dictionary_p)):
        kw_count[kw] = [0,0]
        kw_score[kw] = [0,0]

    for p in p_text:
        kw_pos = sw.participle(p)
        entries = []
        for kw in kw_pos:
            if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
                entries.append(kw[0])
        if entries != []:
            bow = dictionary_p.doc2bow(entries)
            for pair in bow:
                try:
                    kw_count[pair[0]][0] += pair[1]
                except:
                    print pair

    for n in n_text:
        kw_pos = sw.participle(n)
        entries = []
        for kw in kw_pos:
            if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
                entries.append(kw[0])
        if entries != []:
            bow = dictionary_p.doc2bow(entries)
            for pair in bow:
                try:
                    kw_count[pair[0]][1] += pair[1]
                except:
                    print pair
    
    total = [0,0]
    for kw in range(len(dictionary_p)):
        total[0] += (kw_count[kw][0]+1)
        total[1] += (kw_count[kw][1]+1)

    kw_file = file('./classify_dict/second_classify.txt','a')
    for kw in range(len(dictionary_p)):
        kw_score[kw][0] += (kw_count[kw][0]+1)/total[0]
        kw_score[kw][1] += (kw_count[kw][1]+1)/total[1]
        kw_file.write(str(kw)+' '+str(kw_score[kw][0])+' '+str(kw_score[kw][1])+'\n')

    kw_file.close()

def main_three(p_text,n_text,e_text,v_text,c_text):#政治、外交、经济
  
    dictionary_p = corpora.Dictionary([])
    print len(p_text),len(n_text),len(e_text),len(v_text),len(c_text)

    for p in p_text:
        kw_pos = sw.participle(p)
        entries = []
        for kw in kw_pos:
            if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
                entries.append(kw[0])
        dictionary_p.add_documents([entries])

    for n in n_text:
        kw_pos = sw.participle(n)
        entries = []
        for kw in kw_pos:
            if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
                entries.append(kw[0])
        dictionary_p.add_documents([entries])

    for e in e_text:
        kw_pos = sw.participle(e)
        entries = []
        for kw in kw_pos:
            if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
                entries.append(kw[0])
        dictionary_p.add_documents([entries])

    for v in v_text:
        kw_pos = sw.participle(v)
        entries = []
        for kw in kw_pos:
            if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
                entries.append(kw[0])
        dictionary_p.add_documents([entries])

    for c in c_text:
        kw_pos = sw.participle(c)
        entries = []
        for kw in kw_pos:
            if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
                entries.append(kw[0])
        dictionary_p.add_documents([entries])

    dictionary_p.filter_extremes(10,0.7,1000000)
    dictionary_p.compactify()
    dictionary_p.save('./classify_dict/new_classify.dict')

    kw_count = dict()
    kw_score = dict()
    for kw in range(len(dictionary_p)):
        kw_count[kw] = [0,0,0,0,0]
        kw_score[kw] = [0,0,0,0,0]

    for p in p_text:
        kw_pos = sw.participle(p)
        entries = []
        for kw in kw_pos:
            if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
                entries.append(kw[0])
        if entries != []:
            bow = dictionary_p.doc2bow(entries)
            for pair in bow:
                try:
                    kw_count[pair[0]][0] += pair[1]
                except:
                    print pair

    for n in n_text:
        kw_pos = sw.participle(n)
        entries = []
        for kw in kw_pos:
            if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
                entries.append(kw[0])
        if entries != []:
            bow = dictionary_p.doc2bow(entries)
            for pair in bow:
                try:
                    kw_count[pair[0]][1] += pair[1]
                except:
                    print pair

    for e in e_text:
        kw_pos = sw.participle(e)
        entries = []
        for kw in kw_pos:
            if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
                entries.append(kw[0])
        if entries != []:
            bow = dictionary_p.doc2bow(entries)
            for pair in bow:
                try:
                    kw_count[pair[0]][2] += pair[1]
                except:
                    print pair

    for v in v_text:
        kw_pos = sw.participle(v)
        entries = []
        for kw in kw_pos:
            if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
                entries.append(kw[0])
        if entries != []:
            bow = dictionary_p.doc2bow(entries)
            for pair in bow:
                try:
                    kw_count[pair[0]][3] += pair[1]
                except:
                    print pair

    for c in c_text:
        kw_pos = sw.participle(c)
        entries = []
        for kw in kw_pos:
            if kw[1] in cx_dict and (len(kw[0]) > 3 or kw[0] in single_word_whitelist) and kw[0] not in black_word:
                entries.append(kw[0])
        if entries != []:
            bow = dictionary_p.doc2bow(entries)
            for pair in bow:
                try:
                    kw_count[pair[0]][4] += pair[1]
                except:
                    print pair
    
    total = [0,0,0,0,0]
    for kw in range(len(dictionary_p)):
        total[0] += (kw_count[kw][0]+1)
        total[1] += (kw_count[kw][1]+1)
        total[2] += (kw_count[kw][2]+1)
        total[3] += (kw_count[kw][3]+1)
        total[4] += (kw_count[kw][4]+1)

    kw_file = file('./classify_dict/new_classify.txt','a')
    for kw in range(len(dictionary_p)):
        kw_score[kw][0] += (kw_count[kw][0]+1)/total[0]
        kw_score[kw][1] += (kw_count[kw][1]+1)/total[1]
        kw_score[kw][2] += (kw_count[kw][2]+1)/total[2]
        kw_score[kw][3] += (kw_count[kw][3]+1)/total[3]
        kw_score[kw][4] += (kw_count[kw][4]+1)/total[4]
        kw_file.write(str(kw)+' '+str(kw_score[kw][0])+' '+str(kw_score[kw][1])+' '+str(kw_score[kw][2])+' '+str(kw_score[kw][3])+' '+str(kw_score[kw][4])+'\n')

    kw_file.close()

def get_data(d_time):

    reader = csv.reader(file('./news_dict/%s.csv' % d_time, 'rb'))
    text_list = []
    for line in reader:
        text_list.append(line[0])

    return text_list
    
    
if __name__ == '__main__':

    data_first = ['economic','diplomacy','politics','violence','coup']
    #data_second = ['violence','coup']

    text_first = []
    for d_time in data_first:
        text_list = get_data(d_time)
        text_first.append(text_list)

    main_three(text_first[2],text_first[1],text_first[0],text_first[3],text_first[4])

##    text_second = []
##    for d_time in data_second:
##        text_list = get_data(d_time)
##        text_second.append(text_list)
##
##    main_two(text_second[0],text_second[1])
        
