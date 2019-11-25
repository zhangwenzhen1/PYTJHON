import pandas as pd
import numpy as np

r4 = pd.read_csv('D:\guangdong\zhoumangshi1224-1230.csv',encoding='gbk')
r4 = r4.drop_duplicates('小区ID')
r4 = r4[['小区ID','上行日流量(MB)', '下行日流量(MB)']]

gaoxiao = pd.read_csv('D:\guangdong\gaoxiao_1.csv',encoding='gbk')
gaoxiao  = gaoxiao.drop_duplicates('ECGI')
print(gaoxiao.iloc[:,0].size)

zb12 = pd.merge(gaoxiao,r4,left_on='ECGI',right_on='小区ID',how='left',suffixes=('', '_y')) # pandas csv表左连接
zb12['日流量GB'] = (zb12['上行日流量(MB)'] + zb12['下行日流量(MB)'])/1024
zb12 = zb12.drop_duplicates()
zb12 =zb12.loc[zb12['日流量GB'].notnull() & zb12['日流量GB']!=0]
print(zb12.iloc[:,0].size)
zb12.to_csv('D:\guangdong\yyyyyy2.csv',header=1,encoding='gbk') #保存列名存储
