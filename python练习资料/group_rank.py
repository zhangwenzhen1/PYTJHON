import pandas as pd

df = pd.read_csv('D:\guangdong\dishi1224-1230.csv',encoding='gbk')
print(df.columns)
df['Throughput_sort']= df['日流量GB'].groupby(df['地市']).rank(ascending=0,method='dense')
df['Utilization_rate_sort']= df['最大利用率'].groupby(df['地市']).rank(ascending=0,method='dense')
print(df)
# df.to_csv('D:\guangdong\df.csv',header=1,encoding='gbk') #保存列名存储
df = df.loc[((df['制式标识']=='TDD') &((df['Throughput_sort']==1)|(df['Utilization_rate_sort']==1))),
            ['地市','制式标识', '日流量GB', '最大利用率','Throughput_sort','Utilization_rate_sort']]
print(df)
df.to_csv('D:\guangdong\df1.csv',header=1,encoding='gbk') #保存列名存储
