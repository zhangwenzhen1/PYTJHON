import re
import numpy as np
import pandas as pd
# S= 'AA,BB,EE,DD,AA,ABC,CC,ABC'
# # print(type(S))
# # L=re.split(r', | ',S)
# L=re.split(',',S)
# b=list(set(L))
# print(b)
# # print(L)
# # [x for x in L if L.count(x)==1]
# # print(L)
# # for x in L:
# #     if L.count(x)==1:
# #         print(L)
# #     print(x)
# # print(a)
# # b=list(set(L))
# # print(b)
# d= ','.join(list(set(L)))
# print(d)

# df_temp1 = pd.read_csv('D:\gxt\df_temp1.csv',encoding='gbk')
#
# df_temp1['使用频段'] =df_temp1['使用频段'].apply(lambda x: x.replace('DC', 'FDD1800'))
# #####物理站点频段统计
# gg1 = df_temp1.groupby(by='物理站名').apply(lambda x:','.join(x['使用频段']))
# gg1 = gg1.to_frame()
# gg1= gg1.reset_index(drop=False)
# gg1.columns=['物理站名','频段类']
# print(gg1.head())
# def f(x):
#     L = re.split(',', x)
#     d = ','.join(list(set(L)))
#     return d
# print(type(gg1['频段类']))
#
# gg1['频段类'] = gg1['频段类'].apply(lambda x: f(x))
# gg1.to_csv('D:\gxt\df6.csv',header=1,encoding='gbk') #保存列名存储.to_csv('D:\gxt\df2.csv',header=1,encoding='gbk') #保存列名存储
# S ='D,F,FDD'
# a ='D,F'
# b ='D'



g3 = pd.read_csv('D:\gxt\df9.csv',encoding='gbk') #保存列名存储
print(g3.iloc[:,0].size)
print(g3.head())
g3_temp =g3.loc[g3['是否共址共向小区']=='待定']
print(g3_temp.head())
print(g3_temp.iloc[:,0].size)
g3_temp1 = g3_temp.groupby(by=['物理站名','同向小区数']).apply(lambda x:','.join(x['使用频段']))
gg1_temp = g3_temp1.to_frame()
gg1_temp= gg1_temp.reset_index(drop=False)
gg1_temp.columns=['物理站名','同向小区数','频段类1']
print(gg1_temp.head())

def f(x):
    L = re.split(',', x)
    d = ','.join(list(set(L)))
    return d

gg1_temp['频段类1'] = gg1_temp['频段类1'].apply(lambda x: f(x))
gg1_temp['aa'] =np.where(gg1_temp['频段类1']=='D,F','D+F共向，D+F+FDD不共向',
                         np.where(gg1_temp['频段类1']=='D,FDD1800','D+FDD共向，D+F+FDD不共向',
                                  np.where(gg1_temp['频段类1']=='F,FDD1800','F+FDD共向，D+F+FDD不共向','D+F+FDD共向')))
print(gg1_temp.columns)
gg1_temp = pd.merge(g3_temp,gg1_temp,on=['物理站名','同向小区数'],how='left',suffixes=('', '_y')) # pandas csv表左连接
print(gg1_temp.head())
gg1_temp.rename(columns={'Unnamed: 0': '序号'},inplace=True)
gg1_temp.set_index('序号',inplace=True)
print(gg1_temp.head())
gg1_temp =gg1_temp[['aa']]
df = pd.merge(g3,gg1_temp,right_index=True, left_index=True,how ='outer',suffixes=('', '_y'))
df['是否共址共向小区'] =np.where(df['是否共址共向小区']=='待定',df['aa'],df['是否共址共向小区'])

print(df.head())
# df.to_csv('D:\gxt\df13.csv',header=1,encoding='gbk') #保存列名存储.to_csv('D:\gxt\df2.csv',header=1,encoding='gbk') #保存列名存储