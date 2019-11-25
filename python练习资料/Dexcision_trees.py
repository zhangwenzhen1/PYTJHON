from math import log
import operator

def calcShannonEnt(dataSet):  # 计算数据的熵(entropy)
    numEntries=len(dataSet)  # 数据条数
    labelCounts={}
    for featVec in dataSet:
        currentLabel=featVec[-1] # 每行数据的最后一个字（类别）
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1  # 统计有多少个类以及每个类的数量
    shannonEnt=0
    for key in labelCounts:
        prob=float(labelCounts[key])/numEntries # 计算单个类的熵值
        shannonEnt-=prob*log(prob,2) # 累加每个类的熵值
    return shannonEnt

def createDataSet1():    # 创造示例数据
    dataSet = [['长', '粗', '男'],
               ['短', '粗', '男'],
               ['短', '粗', '男'],
               ['长', '细', '女'],
               ['短', '细', '女'],
               ['短', '粗', '女'],
               ['长', '粗', '女'],
               ['长', '粗', '女']]
    labels = ['头发','声音']  #两个特征
    return dataSet,labels

def splitDataSet(dataSet,axis,value): # 按某个特征分类后的数据
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            reducedFeatVec =featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):  # 选择最优的分类特征
    numFeatures = len(dataSet[0])-1
    baseEntropy = calcShannonEnt(dataSet)  # 原始的熵
    bestInfoGain = 0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)
            prob =len(subDataSet)/float(len(dataSet))
            newEntropy +=prob*calcShannonEnt(subDataSet)  # 按特征分类后的熵
        infoGain = baseEntropy - newEntropy  # 原始熵与按特征分类后的熵的差值
        if (infoGain>bestInfoGain):   # 若按某特征划分后，熵值减少的最大，则次特征为最优分类特征
            bestInfoGain=infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):    #按分类后类别数量排序，比如：最后分类为2男1女，则判定为男；
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]  # 类别：男或女
    if classList.count(classList[0])==len(classList):  #停止条件一：判断所有类别标签是否相同，完全相同则停止继续划分
        return classList[0]
    if len(dataSet[0])==1:     #停止条件二：遍历完所有特征时返回出现次数最多的
        return majorityCnt(classList)
    bestFeat=chooseBestFeatureToSplit(dataSet) #选择最优特征
    bestFeatLabel=labels[bestFeat]
    myTree={bestFeatLabel:{}} #分类结果以字典形式保存
    del(labels[bestFeat])
    featValues=[example[bestFeat] for example in dataSet]
    uniqueVals=set(featValues)
    for value in uniqueVals:
        subLabels=labels[:]
        myTree[bestFeatLabel][value]=createTree(splitDataSet\
                            (dataSet,bestFeat,value),subLabels)
    return myTree


if __name__=='__main__':
    dataSet, labels=createDataSet1()  # 创造示列数据
    print(createTree(dataSet, labels))  # 输出决策树模型结果



#############################################
'''
#coding=utf-8
from math import log
import numpy as np
import operator
import pandas as pd

# 数据准备
filename = 'data.csv'
def creatDataSet(filename):
    df = pd.DataFrame(pd.read_csv(filename))
    # 数据转换将属性转化为0,1标称数据类型
    outLook_mapping = {label: idx for idx, label in enumerate(set(df['Outlook']))}
    windy_mapping = {label: idx for idx, label in enumerate(set(df['Windy']))}
    play_mapping = {label: idx for idx, label in enumerate(set(df['PlayGoIf?']))}
    df['Outlook'] = df['Outlook'].map(outLook_mapping)
    df['Windy'] = df['Windy'].map(windy_mapping)
    df['PlayGoIf?'] = df['PlayGoIf?'].map(play_mapping)
    numberOfLines = len(df)
    # 数据矩阵初始化
    dataSet = np.zeros((numberOfLines, 5))
    # 类别数组初始化
    classLabelVector = []
    classLabelVector.extend(df.columns[0:4])
    index = 0
    for row in df.values:
        dataSet[index, :] = row[0:5]
        index += 1
    return list(dataSet),classLabelVector

# 计算给定数据集合的香农熵
def calcShannonEnt(dataset):
    numEntries = len(dataset)
    # 空字典用于统计类别
    labelCounts = {}
    for featVec in dataset:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries #使用频率pi
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt

#按照给定特征划分数据集
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVecn in dataSet:
        featVec = list(featVecn)
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

#选择最好的数据集划分方式
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    basicEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):        #计算每一个特征的熵增益
        featlist = [example[i] for example in dataSet]
        uniqueVals = set(featlist)
        newEntropy = 0.0
        for value in uniqueVals:        #计算每一个特征的不同取值的熵增益
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet) #不同取值的熵增加起来就是整个特征的熵增益
        infoGain = basicEntropy - newEntropy
        if (infoGain > bestInfoGain):   #选择最高的熵增益作为划分方式
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

#选择出类别出现最多的分类
def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key = operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList): #停止条件一：判断所有类别标签是否相同，完全相同则停止继续划分
        return classList[0]
    if len(dataSet[0]) == 1:    #停止条件二：遍历完所有特征时返回出现次数最多的
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)    #得到列表包含的最佳属性值
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree


dataSet, labels = creatDataSet(filename)
myTree = createTree(dataSet, labels)
print(myTree)

'''