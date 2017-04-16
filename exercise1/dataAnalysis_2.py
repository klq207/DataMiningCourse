# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from math import isnan, sqrt
import matplotlib.pyplot as plt
import pylab
import scipy.stats as stats

numeric_attr = []
non_numeric_attr = []

#将'?'转换为nan
def nan_convert(x):
    if x == '?':
        return np.nan
    else:
        return float(x)

# 计算a和b之间的欧几里得距离
def distance(a, b):
    dist = 0.0
    for i in range(3, len(a)):
        if isnan(a[i]) == True and isnan(b[i]) == True:
            return 1000000
        if isnan(a[i]) == True or isnan(b[i]) == True:
            continue
        dist = dist + (a[i] - b[i]) * (a[i] - b[i])
    return sqrt(dist)



# 用b来填补a
def patch(a, b):
    ret = []
    for i in range(len(a)):
        if isnan(a[i]) == True:
            ret.append(b[i])
        else:
            ret.append(a[i])
    return ret

# 找第二相关的属性
def find_second_big(a):
    max_value, index = -1, 0
    for i in range(len(a)):
        if max_value < a[i] and a[i] < 1:
            max_value = a[i]
            index = i
    return index

# 不同方式的数据缺失处理
def replace_default(data, type):
    if type == 0:
        for attr in numeric_attr:
            data[attr] = Series(map(nan_convert, list(data[attr])))
        for attr in non_numeric_attr:
            data[attr] = Series(map(nan_convert, list(data[attr])))
    elif type == 1:  # delete missing value
        return data.dropna()
    elif type == 2:
        for attr in numeric_attr:
            element, num = 0.01, -1
            tmp = list(data[attr])
            # 找出出现频率最高的
            for x in data[attr].unique():
                if x == np.nan:
                    continue
                elif tmp.count(x) > num:
                    num = tmp.count(x)
                    element = x
            data[attr] = data[attr].replace(np.nan, element)
        for attr in non_numeric_attr:
            element, num = 0.01, -1
            tmp = list(data[attr])
            # 找出出现频率最高的
            for x in data[attr].unique():
                if x == np.nan:
                    continue
                elif tmp.count(x) > num:
                    num = tmp.count(x)
                    element = x
            data[attr] = data[attr].replace(np.nan, element)
        return data
    elif type == 3:
        data1 = data[numeric_attr]
        cor_data = data1.corr()
        print cor_data
        for attr in numeric_attr:
            tmp = pd.isnull(data[attr])
            if True not in list(tmp):
                continue
            index = find_second_big(cor_data[attr])
            data[attr] = patch(data[attr], data[numeric_attr[index]])
        return data
    elif type == 4:
        for i in range(len(data)):
            tmp = pd.isnull(data.iloc[i])
            if True not in list(tmp):
                continue
            else:
                min_dis, min_index = 10000000.0, 0
                for j in range(len(data)):
                    if i == j:
                        continue
                    else:
                        dis = distance(data.iloc[i], data.iloc[j])
                        if min_dis > dis:
                            min_dis = dis
                            min_index = j
                data.iloc[i] = patch(data.iloc[i], data.iloc[min_index])
        return data

# 缺失值统计
def missing_count(data):
    print ('count missing value')
    for attr in numeric_attr:
        num = 0
        for x in data[attr]:
            if isnan(x) == True:
                num = num + 1
        print (attr, num)
    for attr in non_numeric_attr:
        num = 0
        for x in data[attr]:
            if isnan(x) == True:
                num = num + 1
        print (attr, num)

# 标称属性数据摘要
def data_abstract(feature, unique_feature):
    for s in unique_feature:
        print (s, feature.count(s))


# 数值属性数据摘要
def data_abstract_numeric(data):
    print ('max value: ', data.max())
    print ('min value: ', data.min())
    print ('median value: ', data.median())
    print ('quantile(0.25): ', data.quantile(0.25))
    print ('quantile(0.75): ', data.quantile(0.75))

# 绘制直方图和qq图
def plot_histogram(data1, title, intro):
    # 绘制直方图
    plt.hist(data1, bins=20, color='green', normed=False)
    plt.xlabel(title)
    plt.ylabel('value')
    plt.savefig(intro+'/histogram_pic/'+title+'_histogram.jpg')
    plt.clf()
    #plt.show()
    # 绘制qq图
    stats.probplot(data1, dist="norm", plot=pylab)
    pylab.xlabel(title)
    pylab.ylabel('value')
    pylab.savefig(intro+'/qq_pic/'+title+'_qq.jpg')
    pylab.clf()
    #pylab.show()

# 绘制盒图
def plot_box(data1, title,intro):
    plt.title('Box plot')
    data = []
    for i in data1:
        data.append(i)
    plt.boxplot(data, notch=False, sym='rs', vert=True)
    plt.xlabel(title)
    plt.ylabel('value')
    plt.savefig(intro+'/box_pic/'+title+'_box.jpg')
    plt.clf()
    #plt.show()


def visualization(data,intro):
    # 标称属性摘要
    print ('count non-numeric attributes value')
    for attr in non_numeric_attr:
        s = list(data[attr])
        data_abstract(s, Series(s).unique())

    # 数值属性摘要
    print ('count numeric attributes value')
    for attr in numeric_attr:
        print ('attribute: ' + attr)
        data_abstract_numeric(data[attr])

    # 绘制直方图
    for attr in numeric_attr:
        plot_histogram(data[attr], attr, intro)

    # 绘制盒图
    for attr in numeric_attr:
        plot_box(data[attr], attr, intro)

# 丢弃数据中的某些行
def drop_data(data):
    for i in range(0,368):
        num = 0
        for j in data.ix[i]:
            if isnan(j) == True:
                num = num + 1
        print num
        if num > 1:
            data = data.drop([i])
    return data

# 处理原始数据
# f1 = open('data/horse-colic-all.data','r')
# text = f1.read()
# text = text.replace(" ",",")
# f1.close()
# f2 = open('data/horse-colic-all.csv','w')
# f2.write(text)
# f2.close()

# 读取csv数据，将缺失值替换为nan，计算缺失值数目
data = pd.read_csv('data/horse-colic-all.csv');
column = list(data.columns)
non_numeric_attr = column[0:3]+column[6:15]+column[16:18]+column[20:21]+column[22:30]
numeric_attr = column[3:6]+column[15:16]+column[18:20]+column[21:22]
replace_default(data, 0)
missing_count(data)

# # 将缺失部分剔除
# data1 = data.copy()
# data1 = replace_default(data1, 1)
# visualization(data1,'removeBlank_pic_2')
# data1.to_csv('delete_2.csv')
# del data1
#
# # 用最高频率值来填补缺失值
# data1 = data.copy()
# data1 = replace_default(data1, 2)
# visualization(data1, 'maxFrequency_pic_2')
# data1.to_csv('fill_fre_2.csv')
# del data1

# 通过属性的相关关系来填补缺失值
data = drop_data(data)
data.index = range(len(data))
data1 = data.copy()
data1 = replace_default(data1, 3)
visualization(data1, 'attrRelative_pic_2')
data1.to_csv('fill_att_2.csv')
del data1

# 通过数据对象之间的相似性来填补缺失值
# data1 = data.copy()
# data1 = replace_default(data1, 4)
# visualization(data1, 'dataSimilarity_pic_2')
# data1.to_csv('fill_simi_2.csv')
# del data1