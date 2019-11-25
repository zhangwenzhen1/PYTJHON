import pandas as pd
import numpy as np
df  = pd.read_csv('D:\Volte.table_names.csv',encoding='gbk')
print(df.head())
# df1 = df.loc[(df['mode'] =='无线') | (d['mode'] =='性能分析')]
df = df.groupby(by='tablename').apply(lambda x:','.join(x['columnname']))
print(df.head())
df.to_csv('D:\Volte.table_names1.csv',header=1,index=True,encoding='gbk',)