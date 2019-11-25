import pandas as pd
import os
import numpy as np
###########################################################
df = pd.read_csv('D:\Volte_v600_20190817.csv',encoding='utf-8',sep='|',error_bad_lines=False)
df = df.rename(columns=lambda x: x.replace(" ","").replace("'",""))
print(df.iloc[:,0].size)
df.drop(['Unnamed:0'],axis=1,inplace=True)
df['accept_msisdn'] = df['accept_msisdn'].astype('str')
df['accept_msisdn']= df['accept_msisdn'].map(str.strip) #清空空格
df = df.loc[(df['accept_msisdn'] != 'accept_msisdn')]
df = df.loc[(~df['report_time'].isnull())]
print(df.iloc[:,0].size)
# df = df.drop_duplicates('accept_msisdn')
# df['p.problem_sort']=df['p.problem_sort'].map(str.strip) #清空空格
# df = df.loc[(df['p.problem_sort'] != 'p.problem_sort')]
# df['投诉分类'] = df['k.service_type_cd'].str[0:10]
df.to_csv('D:\V6001.csv',header=1,encoding='gbk',index=False) #保存列名存储
# df['投诉分类'] = df['投诉分类'].astype('int')
# df['2,3,4G投诉'] =np.where(df['投诉分类']==401004016,'4G',
#                          np.where(df['投诉分类']== 401004015,'2,3G',
#                                   np.where(df['投诉分类']== 401004003,'volte功能','其他'))
#                          )
# df_1 = df.groupby(['p.problem_sort'])['accept_msisdn'].count()
# df_2 = df.groupby(['2,3,4G投诉'])['accept_msisdn'].count()
#
# writer = pd.ExcelWriter('D:\V60017.xlsx')
# df.to_excel(writer,'投诉详单表',index=False,encoding='gbk')
# df_1.to_excel(writer,'投诉分类表',index=True,encoding='gbk')
# df_2.to_excel(writer,'投诉234G分类表',index=True,encoding='gbk')
# writer.save()
# print(df.iloc[:,0].size)
########################################################################################



# df = pd.read_csv('D:\TTongji0826.csv',encoding='utf-8',sep=',',error_bad_lines=False)
# df = df.drop_duplicates()
# df.to_csv('D:\V6.csv',header=1,encoding='gbk',index=False) #保存列名存储
# print(df.iloc[:,0].size)
# print(df.head())
# print(df.info())
# print(df.iloc[:,0].size)
# df1 = df.loc[df['domaintype']!='无线']
# df = df.loc[df['domaintype']=='无线']
#
# df_0 = df.groupby('failresult')['failcount'].agg(np.sum)
# df_1 = df.groupby('cgi')['failcount'].agg(np.sum)
# df_2 = df.groupby('reason')['failcount'].agg(np.sum)
# df_3 = df1.groupby('domaintype')['failcount'].agg(np.sum)
#
# # sort_values(by="failcount",ascending=False)
#
# print(df_1.head(100))
#
#
# writer_1 = pd.ExcelWriter('D:\Vtongjibiao2.xlsx')
# df_0.to_excel(writer_1,'投诉失败分类表',index=True,encoding='gbk')
# df_1.to_excel(writer_1,'投诉无线分类表',index=True,encoding='gbk')
# df_2.to_excel(writer_1,'投诉问题分类表',index=True,encoding='gbk')
# df_3.to_excel(writer_1,'域表',index=True,encoding='gbk')
# # df_2.to_excel(writer,'投诉234G分类表',index=True,encoding='gbk')
# writer_1.save()
