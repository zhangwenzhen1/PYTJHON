import numpy as np
import pandas as pd

zb = pd.read_csv('D:\guangdong\liuliangxishu.csv',encoding='gbk')

fz = zb.loc[(zb['最大利用率']>0.5) & (zb['地市'].notnull()), ['地市','小区ID','上行PRB平均利用率(v2.8)',
                                                       '下行PRB平均利用率(v2.8)','PDCCH信道CCE占用率','最大利用率']]
fz1 = fz.loc[(fz['上行PRB平均利用率(v2.8)']>fz['下行PRB平均利用率(v2.8)']),['地市','小区ID','上行PRB平均利用率(v2.8)',
                                                       '下行PRB平均利用率(v2.8)','PDCCH信道CCE占用率','最大利用率']]
fz1.to_csv('D:\guangdong\Fz1.csv',header=1,encoding='gbk') #保存列名存储
f_mean1 = fz1['上行PRB平均利用率(v2.8)'].mean()
f_mean2 = fz1['下行PRB平均利用率(v2.8)'].mean()
fz_0 = fz.groupby('地市')['小区ID'].count()
fz_1 = fz1.groupby('地市')['小区ID'].count()
fz_0 = fz_0.to_frame()
fz_1 = fz_1.to_frame()
fz1_temp1 = fz1.groupby('地市')['上行PRB平均利用率(v2.8)'].agg([np.mean])
fz1_temp2 = fz1.groupby('地市')['下行PRB平均利用率(v2.8)'].agg([np.mean])
fzb = pd.merge(fz_0,fz_1,on='地市',how='left',suffixes=('', '_y')) # pandas csv表左连接
fzb = pd.merge(fzb,fz1_temp1,on='地市',how='left',suffixes=('', '_y')) # pandas csv表左连接
fzb = pd.merge(fzb,fz1_temp2,on='地市',how='left',suffixes=('', '_y')) # pandas csv表左连接
fzb.columns = ['周平均高负荷小区数','上行高负荷小区数','上行高负荷小区-平均上行利用率','上行高负荷小区-平均下行利用率']
fzb.loc['全省'] = fzb.apply(lambda x: x.sum())
fzb['上行高负荷小区占比'] = fzb['上行高负荷小区数']/fzb['周平均高负荷小区数']
fzb = fzb.reindex(['全省','广州','深圳','东莞','佛山','汕头','珠海','惠州','中山','江门','湛江','茂名','揭阳','韶关','河源','梅州','汕尾','阳江','肇庆','清远','潮州','云浮'])
fzb = fzb[['周平均高负荷小区数','上行高负荷小区数','上行高负荷小区占比','上行高负荷小区-平均上行利用率','上行高负荷小区-平均下行利用率']]
fzb.iat[0,3] = f_mean1
fzb.iat[0,4] = f_mean2
print(fzb.head(22))
fzb.to_csv('D:\guangdong\gfhlyb.csv',header=1,encoding='gbk') #保存列名存储
# print(fz1_temp2.head())