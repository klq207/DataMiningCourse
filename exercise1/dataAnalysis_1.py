# -*- coding: utf-8 -*-
import numpy as np
import pylab
import scipy.stats as stats
import string
import math
import matplotlib.pyplot as plt
H_attrNames = ["null","surgery", "Age", "Hospital Number", "rectal temperature", \
               "pulse", "respiratory rate", "temperature of extremities", "peripheral pulse", \
               "mucous membranes", "capillary refill time", "pain", "peristalsis", \
               "abdominal distension", "nasogastric tube", "nasogastric reflux", "nasogastric reflux PH", \
               "rectal examination", "abdomen", "packed cell volume", "total protein", \
               "abdominocentesis appearance", "abdomcentesis total protein", "outcome", "surgical lesion", \
               "type of lesion", "type of lesion", "type of lesion", "cp_data"]
NominalL = [1,2,3,7,8,9,10,11,12,13,14,15,17,18,21,23,24,25,26,27,28]
NumericalL = [4,5,6,16,19,20,22]
samples = [] #读入的所有样本


#缺失值处理：将缺失部分剔除
def removeBlank():
    # 对所有标称属性进行分析
    for j in NominalL:
        num = []
        for sample in samples:
            if sample[j - 1] != "?":
                num.append(sample[j - 1])
        print H_attrNames[j]+"："
        print nominal_analysis(num)
    # 对所有数值属性进行分析
    for k in NumericalL:
        blankcount = 0
        num = []
        for sample in samples:
            if sample[k - 1] != "?":
                num.append(string.atof(sample[k - 1]))
            else:
                blankcount = blankcount + 1
        print H_attrNames[k]+"："
        print numerical_analysis(num,k,blankcount)
        visualization_pic(num, k, 'removeBlank_pic_1')

    return

# 得到出现频率最高的字符串
def max_freq_str(num):
    dict = {}
    for ni in num:
        if ni != "?":
            if ni in dict.keys():
                dict[ni] = dict[ni] + 1
            else:
                dict[ni] = 1

    fre_str = sorted(dict.items(), key=lambda e: e[1], reverse=True)[0][0]
    return fre_str

#缺失值处理：用最高频率值来填补缺失值
def maxFrequency():
    new_samples = samples
    # 对所有标称属性进行分析
    for j in NominalL:
        num = []
        for sample in new_samples:
            if sample[j - 1] != "?":
                num.append(sample[j - 1])
        fre_str = max_freq_str(num)
        for sample in new_samples:
            if sample[j - 1] == "?":
                sample[j - 1] = fre_str
        for sample in new_samples:
                num.append(sample[j - 1])
        print H_attrNames[j] + "："
        print nominal_analysis(num)

    # 对所有数值属性进行分析
    for k in NumericalL:
        num = []
        for sample in new_samples:
            if sample[k - 1] != "?":
                num.append(string.atof(sample[k - 1]))
        q1,q2,q3 = quartile(num)
        ave = float("%.2f" % np.mean(num))
        #对于正态分布（特征4和特征10）用均值填补，对偏态分布用中位数填补
        num = []
        if k == 4 or k == 10:
            for sample in new_samples:
                if sample[k - 1] == "?":
                    sample[k - 1] = ave
                num.append(string.atof(sample[k - 1]))
        else:
            for sample in new_samples:
                if sample[k - 1] == "?":
                    sample[k - 1] = q2
                num.append(string.atof(sample[k - 1]))
        print H_attrNames[k] + "："
        print numerical_analysis(num, k, 0)
        visualization_pic(num, k, 'maxFrequency_pic_1')
    f1 = open('fill_fre_1.txt','w')
    for sample in new_samples:
        for s in sample:
            f1.write(str(s) + " ")
        f1.write("\n")
    f1.close()
    return

# 缺失值处理：通过属性的相关关系来填补缺失值
#def attrRelative():

    #数据缺失情况[2, 0, 0, 69, 26, 71, 65, 83, 48, 38, 63, 52, 65, 131, 133, 299, 128, 143, 37, 43, 194, 235, 2, 0, 0, 0, 0, 0]
    #0代表无缺失，非0表示缺失次数，经统计发现，特征1,4-23都存在缺失数据的情况

    #计算缺失值情况
    # flag = []
    # flag.append(0)
    # for i in range(1,29):
    #     count = 0
    #     for sample in new_samples:
    #         if sample[i-1] == "?":
    #             count = count + 1
    #     flag.append(count)
    # print "flag:"
    # print flag
    # return

# 对标称属性，求每个可能取值的频数
def nominal_analysis(num):
    dict = {}
    for ni in num:
        if ni != "?":
            if ni in dict.keys():
                dict[ni] = dict[ni] + 1
            else:
                dict[ni] = 1
    return dict

# 计算四分位数
def quartile(num):
    na_len = len(num)
    na_q1_index = float(na_len + 1) / 4
    na_q2_index = float(na_len + 1) / 2
    na_q3_index = 3 * float(na_len + 1) / 4
    if na_len % 2 == 1:
        na_q1 = num[int(na_q1_index) - 1]
        na_q2 = num[int(na_q2_index) - 1]
        na_q3 = num[int(na_q3_index) - 1]
    else:
        def cal(index):
            return num[int(math.floor(index)) - 1] + \
                   (num[int(math.ceil(index)) - 1] - num[int(math.floor(index)) - 1]) * (
                       index - math.floor(index))

        na_q1 = cal(na_q1_index)
        na_q2 = cal(na_q2_index)
        na_q3 = cal(na_q3_index)
    return na_q1,na_q2,na_q3

# 对数值属性，给出最大、最小、均值、中位数、四分位数及缺失值的个数
def numerical_analysis(num,nid,blankcount):

    # 计算四分位数
    q1,q2,q3 = quartile(num)

    return max(num),min(num),float("%.2f" % np.mean(num)),(q1,q2,q3),q2,blankcount

# 数据可视化
def visualization_pic(num,nid,intro):
    histogram_pic(num, nid, intro)
    qq_pic(num, nid, intro)
    box_pic(num, nid, intro)
    return

# 绘制直方图
def histogram_pic(num,nid,intro):
    plt.hist(num, bins=20, color='green', normed=False)  # bins显示有几个直方,normed是否对数据进行标准化
    #plt.show()
    plt.xlabel(H_attrNames[nid])
    plt.ylabel('value')
    plt.savefig(intro+'/histogram_pic/'+H_attrNames[nid]+'_histogram.jpg')
    plt.clf()
    return

# 绘制qq图
def qq_pic(num,nid,intro):
    stats.probplot(num, dist="norm", plot=pylab)
    #pylab.show()
    pylab.xlabel(H_attrNames[nid])
    pylab.ylabel('value')
    pylab.savefig(intro+'/qq_pic/'+H_attrNames[nid] + '_qq.jpg')
    pylab.clf()
    return

# 绘制盒图
def box_pic(num,nid,intro):
    plt.boxplot(num,notch=False, sym='rs', vert=True)
    plt.title('Box plot')
    #plt.show()
    plt.xlabel(H_attrNames[nid])
    plt.ylabel('value')
    plt.savefig(intro+'/box_pic/'+H_attrNames[nid] + '_box.jpg')
    plt.clf()
    return

# 读取数据
def read_data():
    f1 = open('data/horse-colic-all.data', 'r')
    txt = f1.readline()
    while txt:
        sample = []
        li = txt[:-1].split()
        for i in range(1, len(li) + 1):
            sample.append(li[i - 1])
        samples.append(sample)
        txt = f1.readline()
    return

if __name__ == '__main__':
    # 读取数据
    read_data()
    # 缺失值处理：将缺失部分剔除
    removeBlank()
    # 缺失值处理：用最高频率值来填补缺失值
    maxFrequency()




