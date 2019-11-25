import pandas as pd
import numpy as np
import ty

######读取表
df1 = pd.read_csv('D:\zhanjiang\Cl4Gcell.csv',encoding='utf-8')
#########删除重复行
df1 = df1.drop_duplicates('CGI')
df3 = pd.read_csv('D:\zhanjiang\Lcz4Gcell.csv',encoding='gbk')
df3 = df3.drop_duplicates('CGI')

df7 = pd.read_csv('D:\zhanjiang\Addressupdate0725.csv',encoding='gbk')
df7 = df7.drop_duplicates('CGI')
df8 = pd.read_csv('D:\zhanjiang\Addressupdate0726.csv',encoding='gbk')
df8 = df8.drop_duplicates('CGI')
df9 = pd.read_csv('D:\zhanjiang\Addressupdate0727.csv',encoding='gbk')
df9 = df9.drop_duplicates('CGI')
df10 = pd.read_csv('D:\zhanjiang\Addressupdate0728.csv',encoding='gbk')
df10 = df10.drop_duplicates('CGI')
df11 = pd.read_csv('D:\zhanjiang\Addressupdate0730.csv',encoding='gbk')
df11 = df11.drop_duplicates('CGI')
df12 = pd.read_csv('D:\zhanjiang\Addressupdate0731.csv',encoding='gbk')
df12 = df12.drop_duplicates('CGI')

df13 = pd.read_csv('D:\zhanjiang\Addressupdate0824.csv',encoding='gbk')
df13 = df13.drop_duplicates('CGI')
df14 = pd.read_csv('D:\zhanjiang\Addressupdate0825.csv',encoding='gbk')
df14 = df14.drop_duplicates('CGI')
df15 = pd.read_csv('D:\zhanjiang\Addressupdate0826.csv',encoding='gbk')
df15 = df15.drop_duplicates('CGI')

######LTE位置更新表合并（7天）
df7 = df7.append(df8)
df7 = df7.append(df9)
df7 = df7.append(df10)
df7 = df7.append(df11)
df7 = df7.append(df12)

######LTE位置更新表合并（上周3天）
df10 = df10.append(df11)
df10 = df10.append(df12)

######LTE位置更新表合并（本周周3天）
df13 = df13.append(df14)
df13 = df13.append(df15)

###筛选出7天位置更新出现3次的小区
z7 = df7.groupby(['CGI']).count()
z7 = z7.reset_index(drop=False)
z7 = z7.loc[z7['ECI']>=3,['ECI','CGI']]
z7.columns =['位置更新数','CGI']
print(z7.iloc[:,0].size)
       ######删除重复行
df7 = df7.drop_duplicates('CGI')
df7 = pd.merge(z7,df7,on='CGI',how='left',suffixes=('', '_y')) # pandas csv表左连接
print(df7.iloc[:,0].size)

z10 = df10.groupby(['CGI']).count()
z10 = z10.reset_index(drop=False)
z10 = z10.loc[z10['ECI']>=1,['ECI','CGI']]
z10.columns =['位置更新数','CGI']

print(z10.iloc[:,0].size)
df10 = df10.drop_duplicates('CGI')
df10 = pd.merge(z10,df10,on='CGI',how='left',suffixes=('', '_y')) # pandas csv表左连接
print(df10.iloc[:,0].size)

z13 = df13.groupby(['CGI']).count()
z13 = z13.reset_index(drop=False)
z13 = z13.loc[z13['ECI']>=1,['ECI','CGI']]
z13.columns =['位置更新数','CGI']
print(z13.iloc[:,0].size)
df13 = df13.drop_duplicates('CGI')
df13 = pd.merge(z13,df13,on='CGI',how='left',suffixes=('', '_y')) # pandas csv表左连接
print(df13.iloc[:,0].size)

##4G工参表列名排序
df1['状态'] ='存量'
df1 = df1[['EUTRANCELL名称','所属地市','小区码CI','所属ENODEBID','生命周期状态','工程期数','CGI', '状态','所属规划工单','网络制式','优化网格','所属ENODEB']]
df3['状态'] ='流程中'
df3 = df3[['EUTRANCELL名称','所属地市','小区码CI','所属ENODEBID','生命周期状态','建设工期','CGI', '状态','所属规划工单','网络制式','优化网格','所属ENODEB']]

##4G工参表合并
df1 = df1.append(df3)
##4G工参表与位置更新表合并合并
df7 = pd.merge(df7,df1,on='CGI',how='left',suffixes=('', '_y')) # pandas csv表左连接
df10 = pd.merge(df10,df1,on='CGI',how='left',suffixes=('', '_y')) # pandas csv表左连接
df13 = pd.merge(df13,df1,on='CGI',how='left',suffixes=('', '_y')) # pandas csv表左连接
df7 = df7.drop_duplicates('CGI')
df10 = df10.drop_duplicates('CGI')
df13 = df13.drop_duplicates('CGI')
print(df7.iloc[:,0].size)
print(df10.iloc[:,0].size)
print(df13.iloc[:,0].size)
###选取需要的列
df7 = df7[['位置更新数','EUTRANCELL名称', '所属地市', '小区码CI', '所属ENODEBID',
       '生命周期状态', '工程期数', 'CGI', '状态', '所属规划工单', '网络制式', '优化网格', '所属ENODEB']]
df10 =df10[['位置更新数','EUTRANCELL名称', '所属地市', '小区码CI', '所属ENODEBID',
       '生命周期状态', '工程期数', 'CGI', '状态', '所属规划工单', '网络制式', '优化网格', '所属ENODEB']]
df13 =df13[['位置更新数','EUTRANCELL名称', '所属地市', '小区码CI', '所属ENODEBID',
       '生命周期状态', '工程期数', 'CGI', '状态', '所属规划工单', '网络制式', '优化网格', '所属ENODEB']]


g7 = df7[['EUTRANCELL名称','CGI','小区码CI','生命周期状态', '工程期数', '状态', '所属规划工单']]
g10 = df10[['EUTRANCELL名称','CGI','小区码CI','生命周期状态', '工程期数', '状态', '所属规划工单']]
g13 = df13[['EUTRANCELL名称','CGI','小区码CI','生命周期状态', '工程期数', '状态', '所属规划工单']]
#########调用function函数，为所属地市为空对应字节补充信息
df7_temp  = ty.function(df7)
print(df7_temp.columns)
df7_temp  = pd.merge(df7_temp,g7,on='CGI',how='left',suffixes=('', '_y')) # pandas csv表左连接
df7_temp  = df7_temp[['位置更新数','EUTRANCELL名称', '所属地市', '小区码CI', '所属ENODEBID',
       '生命周期状态', '工程期数', 'CGI', '状态', '所属规划工单', '网络制式', '优化网格', '所属ENODEB']]
print(df7_temp[['EUTRANCELL名称','小区码CI']].head())
df10_temp = ty.function(df10)
df10_temp  = pd.merge(df10_temp,g10,on='CGI',how='left',suffixes=('', '_y')) # pandas csv表左连接
df10_temp  = df10_temp[['位置更新数','EUTRANCELL名称', '所属地市', '小区码CI', '所属ENODEBID',
       '生命周期状态', '工程期数', 'CGI', '状态', '所属规划工单', '网络制式', '优化网格', '所属ENODEB']]
df13_temp = ty.function(df13) ##allcell(LTE)
df13_temp  = pd.merge(df13_temp,g13,on='CGI',how='left',suffixes=('', '_y')) # pandas csv表左连接
df13_temp  = df13_temp[['位置更新数','EUTRANCELL名称', '所属地市', '小区码CI', '所属ENODEBID',
       '生命周期状态', '工程期数', 'CGI', '状态', '所属规划工单', '网络制式', '优化网格', '所属ENODEB']]

print(df7_temp.iloc[:,0].size)
print(df10_temp.iloc[:,0].size)
print(df13_temp.iloc[:,0].size)
########LTE月增加小区
df_1 = df13_temp.loc[(~df13_temp['CGI'].isin(df7_temp['CGI']))]

#########LTE周增加小区
df_2 = df13_temp.loc[(~df13_temp['CGI'].isin(df10_temp['CGI']))]

df13_temp.to_csv('D:\zhanjiang\AllLTE.csv',header=1,encoding='utf-8',index=False) #保存列名存储
df_1.to_csv('D:\zhanjiang\YzLTE.csv',header=1,encoding='utf-8',index=False)
df_2.to_csv('D:\zhanjiang\ZzLTE.csv',header=1,encoding='utf-8',index=False)



