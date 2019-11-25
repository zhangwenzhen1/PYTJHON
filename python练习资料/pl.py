import pandas as pd
import numpy as np

def xishu(a, b):
    if a == 10:
        b = b * 2
    if a == 15:
        b = b * 20 / 15
    if a == 5:
        b = b * 4
    else:
        b = b
        return b

df1 = pd.read_csv('D:\Test\cell_20180919.csv',encoding='gbk')
df2 = pd.read_csv('D:\Test\cell_20180920.csv',encoding='gbk')
df3 = pd.read_csv('D:\Test\cell_20180927.csv',encoding='gbk')

df4 = pd.read_csv('D:\Test\Fangan.csv',encoding='gbk')

df5 = pd.read_csv('D:\Test\Band_Ifo.csv',encoding='gbk')
df5 = df5[['CGI','载波带宽(MHZ)']]
df = df1.append(df2)
df = df.append(df3)
print(df.columns)
df = df[['CGI','日均流量(GB)','自忙时RRC连接平均数','自忙时峰值利用率', '自忙时RRC连接最大数','上行利用率PUSCH','下行利用率PDSCH','下行利用率PDCCH']]
df = df.groupby(['CGI']).agg(np.mean)
# print(df.iloc[:,0].size)
#湛江日均流量
z  = df['日均流量(GB)'].mean()
df = df.reset_index(drop=False)
df['流量系数'] = df['日均流量(GB)']/z

df = pd.merge(df4,df,on=['CGI'],how='left',suffixes=('', '_y')) # pandas csv表左连接
df = pd.merge(df,df5,on=['CGI'],how='left',suffixes=('', '_y')) # pandas csv表左连接

df['流量系数'] = df.apply(lambda x: xishu(x['载波带宽(MHZ)'], x['流量系数']), axis=1)
print(df.head())
print(df.columns)
# print(df.iloc[:,0].size)
df.to_csv('D:\Test\Result.csv',header=1,encoding='gbk',index=False) #保存列名存储



