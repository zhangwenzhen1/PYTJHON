import pandas as pd
import numpy as np

gf_temp1 = pd.read_csv('D:\guangdong\changqigaofuhexiaoqu_10.csv',encoding='gbk')
gf_temp2 = pd.read_csv('D:\guangdong\changqigaofuhexiaoqu_11.csv',encoding='gbk')
gf_temp3 = pd.read_csv('D:\guangdong\changqigaofuhexiaoqu_09.csv',encoding='gbk')
gf = gf_temp1.append(gf_temp2)
gf = gf.append(gf_temp3)
gf_temp4 =gf.drop_duplicates('小区ID')
print(gf_temp4.iloc[:,0].size)
gf = gf.groupby('小区ID').count()
gf = pd.merge(gf,gf_temp4,on = '小区ID',how='left',suffixes=('', '_y'))
print(gf.columns)
gf.columns = ['小区ID', '出现次数', '地市']
#7-9月出现高负荷的小区数过
gf_1 = gf.groupby('地市')['小区ID'].count()
#长期高负荷小区数
gf_2 = gf.loc[(gf['出现次数']>=2)]
gf_2 = gf_2[['地市','小区ID']]
# print(gf_2.columns)
gf_2.to_csv('D:\guangdong\changqigaofuhexiaoqu.csv',header=1,encoding='gbk',index=False) #保存列名存储
# print(gf_2.iloc[:,0].size)
gf_2 = gf_2.groupby('地市')['小区ID'].count()
gf_1 = gf_1.to_frame()
gf_2 = gf_2.to_frame()
# print(gf_2.columns)
gf_1 = pd.merge(gf_1,gf_2,on='地市',how='left',suffixes=('', '_y')) # pandas csv表左连接
gf_1.loc['全省'] = gf_1.apply(lambda x: x.sum())
gf_1 = gf_1.reindex(['全省','广州','深圳','东莞','佛山','汕头','珠海','惠州','中山','江门','湛江','茂名','揭阳','韶关',
                   '河源','梅州','汕尾','阳江','肇庆','清远','潮州','云浮'])
gf_1.columns = [ '出现高负荷的小区数', '长期高负荷小区数']
gf_1['长期高负荷小区占比'] = gf_1['长期高负荷小区数']/gf_1['出现高负荷的小区数']
gf_1.to_csv('D:\guangdong\changqigaofuhexiaoqukuorongfenbu.csv',header=1,encoding='gbk') #保存列名存储
# print(gf_1.head(100))
# print(gf_1.columns)
# print(gf.iloc[:,0].size)
# print(gf_2.iloc[:,0].size)