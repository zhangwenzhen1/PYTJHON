import numpy as np
import pandas as pd
# df = pd.DataFrame({"id":[1001,1002,1003,1004,1005,1006],
#  "date":pd.date_range('20130102', periods=6),
#   "city":['Beijing ', 'sh', ' guangzhou ', 'Shenzhen', 'shanghai', 'BEIJING '],
#  "age":[23,44,54,32,34,32],
#  "category":['100-A','100-B','110-A','110-C','210-A','130-F'],
#   "price":[4200,np.nan,2133,5433,np.nan,4432]},
#   columns =['id','date','city','category','age','price'])
# df['city'].replace('sh', 'shanghai',inplace=True)
# print(df)

df1 = pd.read_csv('D:\guangdong\m_mro_kpi.csv',encoding='gbk')
df1['starttime'] ='2019-04-01'
print(df1.columns)
print(df1.head())
df1.to_csv('D:\gxt\m_mro_kpi1.csv',header=1,encoding='utf-8',index=False) #保存列名存储