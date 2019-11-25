import pandas as pd
import os
import numpy as np
###########################################################
df = pd.read_csv('D:\oas\oas_tw_kf_20191010.csv',encoding='utf-8',nrows=10,error_bad_lines=False)
df = df.reset_index(drop=False)
# df = df.rename(columns=lambda x: x.replace(" ","").replace("'",""))
print(df.iloc[:,0].size)
# df.drop(['Unnamed:0'],axis=1,inplace=True)
# df['accept_msisdn'] = df['accept_msisdn'].astype('str')
# df['accept_msisdn']= df['accept_msisdn'].map(str.strip) #清空空格
print(df.info())
print(df.head())

df.to_csv('D:\oas\oas_tw_kf.csv.csv',header=1,encoding='gbk',index=False) #保存列名存储