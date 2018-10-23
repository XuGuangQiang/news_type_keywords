#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-06 08:03:05
# @Author  : guangqiang_xu (981886190@qq.com)
# @Version : $Id$

from jieba.analyse import *

def get_news_label(content):
    city_list = []
    label_list = []
    with open("label.txt", "r", encoding='UTF-8') as f:
        label_data = f.readlines()
        for term in label_data:
            split1 = term.split(" ")
            city_list.append(split1[0])
            label = []
            for item in split1[1].split(","):
                label.append(item.strip())
            label_list.append(label)
    set_textrank = []
    set_tf_idf = []
    for keyword, weight in textrank(data, withWeight=True, topK=20):
        set_textrank.append(keyword)

    for keyword, weight in extract_tags(data, withWeight=True, topK=20):
        set_tf_idf.append(keyword)

    keywords = list(set(set_textrank).intersection(set(set_tf_idf)))
    print(keywords)
    count = 0
    label = []
    for item in label_list:
        result = list(set(keywords).intersection(set(item)))
        if len(result) != 0:
            label.append(city_list[count])
        count += 1
    if (len(label) >= 1):
        return ",".join(label)
    else:
        return "其他"
