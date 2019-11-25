import pandas as pd
import numpy as np

#####zhangjiangrongliang
####gaofuhexiaoqu

def zhishi(x):
    x =str(x)
    if 'DC-' in x:
        return 'DC'
    if 'DC1-' in x:
        return 'DC'
    if 'DC2-' in x:
        return 'DC'
    if 'DC3-' in x:
        return 'DC'
    if 'DC4-' in x:
        return 'DC'
    if 'DC5-' in x:
        return 'DC'
    if 'AF-' in x:
        return 'AF'
    if 'GS-' in x:
        return 'GS'
    if 'GS1-' in x:
        return 'GS'
    if 'GS2-' in x:
        return 'GS'
    if 'GS3-' in x:
        return 'GS'
    if 'GS4-' in x:
        return 'GS'
    if 'GS5-' in x:
        return 'GS'

def function(x):
    x = str(x)
    if '-HN' in x:
        return 'NB'
    if '-ZN'in x:
        return 'NB'
    if '-EN'in x:
        return 'NB'

gc_1 = pd.read_csv('D:\guangdong\gc1.csv',encoding='gbk')
gc_2 = pd.read_csv('D:\guangdong\gc2.csv',encoding='gbk')
gc = gc_1.append(gc_2)
wyzt_1 = pd.read_csv('D:\guangdong\wyzt_1.csv',encoding='gbk')
wyzt_2 = pd.read_csv('D:\guangdong\wyzt_2.csv',encoding='gbk')
rl = pd.read_csv('D:\guangdong\zhoumangshi1210-1216.csv',encoding='gbk')
wyzt = wyzt_1.append(wyzt_2)
wyzt = wyzt.drop_duplicates('CGI')
wyzt.columns = ['小区ID','网元状态']
zb = pd.merge(rl,wyzt,on='小区ID',how='left',suffixes=('', '_y')) # pandas csv表左连接
zb = pd.merge(zb,gc,on='小区ID',how='left',suffixes=('', '_y')) # pandas csv表左连接
zb = zb[['地市', '小区ID', '小区名称', '基站ID', '基站名称', '覆盖场景','制式标识', '频段', '载频个数', '载波带宽(MHZ)',
       '经度', '纬度', '方位角', '有效RRC连接平均数', '有效RRC连接最大数', 'RRC连接平均数', 'RRC连接最大数',
       '下行PRB平均利用率(v2.8)', '上行PRB平均利用率(v2.8)', 'PDCCH信道CCE占用率', '下行业务信道流量(MB)',
       '上行业务信道流量(MB)', '无线接通率', '上行日流量(MB)', '下行日流量(MB)', '无线掉线率', 'E-RAB掉线率',
       'E-RAB建立成功率', '切换成功率', '网格', '路测网格', '网元状态', '室内外基站属性']]
zb = zb.drop_duplicates('小区ID')
zb['带宽'] = zb['小区名称'].apply(lambda x: zhishi(x))
zb['NB'] = zb['小区名称'].apply(lambda x: function(x))
zb = zb.loc[(zb['NB'].isnull())]
# 计算日流量
zb['日流量GB'] = (zb['上行日流量(MB)'] + zb['下行日流量(MB)']) / 1024
    ##计算单小区日均流量
zb1 = zb.loc[(zb['日流量GB'] != 0) & (zb['日流量GB'].notnull())]
z_mean = zb1['日流量GB'].mean()
print(z_mean)
zb1 = zb1.groupby('网格')['日流量GB'].agg(np.mean)
zb1.columns = ['网格','网格单小区日均流量GB']
zb['网格单小区日均流量GB'] = zb['网格'].map(zb1)
zb['流量系数'] = zb['日流量GB']/zb['网格单小区日均流量GB']

zb['流量系数'] =np.where(( ( ((zb['制式标识']=='FDD')|(zb['制式标识'].isnull())) & ((zb['带宽']=='DC')|(zb['带宽']=='GS')) ) &(zb['载波带宽(MHZ)'] == 5) ),3*zb['流量系数'],
                      np.where(( ( ((zb['制式标识']=='FDD')|(zb['制式标识'].isnull())) & ((zb['带宽']=='DC')|(zb['带宽']=='GS')) ) &(zb['载波带宽(MHZ)'] == 10) ),1.5*zb['流量系数'],
                               np.where(( ( ((zb['制式标识']=='FDD')|(zb['制式标识'].isnull())) & ((zb['带宽']=='DC')|(zb['带宽']=='GS')) ) &(zb['载波带宽(MHZ)'] == 15) ),zb['流量系数'],
                                        np.where(( ( ((zb['制式标识']=='FDD')|(zb['制式标识'].isnull())) & ((zb['带宽']=='DC')|(zb['带宽']=='GS')) ) &(zb['载波带宽(MHZ)'] == 20) ),zb['流量系数']/1.3,
                                                 np.where(( ( ((zb['制式标识']=='FDD')|(zb['制式标识'].isnull())) & ((zb['带宽']=='DC')|(zb['带宽']=='GS')) ) &(zb['载波带宽(MHZ)'] == 1.4) ),3*zb['流量系数'],
                                                        np.where(( ( ((zb['制式标识']=='FDD')|(zb['制式标识'].isnull())) & (zb['带宽']=='DC')) ) &(zb['载波带宽(MHZ)'].isnull() ),zb['流量系数'],
                                                                 np.where(( ( ((zb['制式标识']=='FDD')|(zb['制式标识'].isnull())) & (zb['带宽']=='GS')) ) &(zb['载波带宽(MHZ)'].isnull() ),3*zb['流量系数'],
                                                                          np.where( (( ((zb['制式标识']=='FDD')&(zb['带宽']=='AF')) |(zb['制式标识']=='TDD') ) & (zb['载波带宽(MHZ)'] == 5) ),4*zb['流量系数'],
                                                                                    np.where( (( ((zb['制式标识']=='FDD')&(zb['带宽']=='AF')) |(zb['制式标识']=='TDD') ) & (zb['载波带宽(MHZ)'] == 10) ),2*zb['流量系数'],
                                                                                              np.where((( ((zb['制式标识']=='FDD')&(zb['带宽']=='AF')) |(zb['制式标识']=='TDD') ) & (zb['载波带宽(MHZ)'] == 15) ),20/15*zb['流量系数'],
                                                                                                       np.where((((zb['制式标识'].isnull()) & (zb['带宽'].isnull()))& (zb['载波带宽(MHZ)'] == 5)),4*zb['流量系数'],
                                                                                                                np.where((((zb['制式标识'].isnull()) & (zb['带宽'].isnull()))& (zb['载波带宽(MHZ)'] == 10)),2*zb['流量系数'],
                                                                                                                         np.where( (((zb['制式标识'].isnull()) & (zb['带宽'].isnull()))& (zb['载波带宽(MHZ)'] == 15)),20/15*zb['流量系数'],zb['流量系数'])))))))))))))

df = zb[['地市', '小区ID','网格','日流量GB','网格单小区日均流量GB','流量系数']]
df = df.loc[(df['网格'].notnull())]
df.to_csv('D:\guangdong\Result\wg_coefficient.csv', header=1, encoding='gbk')  # 保存列名存储
print(df.iloc[:,0].size)

######################################################################################################################################
        #####网格业务均衡统计
w1 = zb.loc[(zb['日流量GB']==0),['网格','小区ID','流量系数']]
w2 = zb.loc[(zb['流量系数'] >0) & (zb['流量系数'] <=0.05) , ['网格','小区ID','流量系数']]
w3 = zb.loc[(zb['流量系数'] >0.05) & (zb['流量系数'] <=0.2), ['网格','小区ID','流量系数']]
w4 = zb.loc[(zb['流量系数'] >0.2) & (zb['流量系数'] <=0.5), ['网格','小区ID','流量系数']]
w5 = zb.loc[(zb['流量系数'] >0.5) & (zb['流量系数'] <=1.5), ['网格','小区ID','流量系数']]
w6 = zb.loc[(zb['流量系数'] >1.5) & (zb['流量系数'] <=3), ['网格','小区ID','流量系数']]
w7 = zb.loc[(zb['流量系数'] >3) & (zb['流量系数'] <=5), ['网格','小区ID','流量系数']]
w8 = zb.loc[(zb['流量系数'] >5), ['网格','小区ID','流量系数']]


w_1 = w1.groupby('网格')['小区ID'].count()
w_2 = w2.groupby('网格')['小区ID'].count()
w_3 = w3.groupby('网格')['小区ID'].count()
w_4 = w4.groupby('网格')['小区ID'].count()
w_5 = w5.groupby('网格')['小区ID'].count()
w_6 = w6.groupby('网格')['小区ID'].count()
w_7 = w7.groupby('网格')['小区ID'].count()
w_8 = w8.groupby('网格')['小区ID'].count()
w_1 = w_1.to_frame()
w_2 = w_2.to_frame()
w_3 = w_3.to_frame()
w_4 = w_4.to_frame()
w_5 = w_5.to_frame()
w_6 = w_6.to_frame()
w_7 = w_7.to_frame()
w_8 = w_8.to_frame()

wg = pd.merge(w_1,w_2,on='网格',how='outer',suffixes=('', '_y'))
wg = pd.merge(wg,w_3,on='网格',how='outer',suffixes=('', '_y'))
wg = pd.merge(wg,w_4,on='网格',how='outer',suffixes=('', '_y'))
wg = pd.merge(wg,w_5,on='网格',how='outer',suffixes=('', '_y'))
wg = pd.merge(wg,w_6,on='网格',how='outer',suffixes=('', '_y'))
wg = pd.merge(wg,w_7,on='网格',how='outer',suffixes=('', '_y'))
wg = pd.merge(wg,w_8,on='网格',how='outer',suffixes=('', '_y'))

wg.columns = ['日流量为0','流量系数大于0小于0.05的小区数','流量系数大于0.05小于0.2的小区数','流量系数0.2~0.5','流量系数0.5~1.5','流量系数1.5~3','流量系数3~5','流量系数>5']
wg.fillna(0,inplace = True)
wg['总小区数'] = wg['日流量为0']+wg['流量系数大于0小于0.05的小区数']+wg['流量系数大于0.05小于0.2的小区数']+wg['流量系数0.2~0.5']+wg['流量系数0.5~1.5']+wg['流量系数1.5~3']+wg['流量系数3~5']+wg['流量系数>5']
wg['网格业务均衡比'] = (wg['流量系数0.2~0.5']+wg['流量系数0.5~1.5']+wg['流量系数1.5~3'])*1.0/(wg['日流量为0']+wg['流量系数大于0小于0.05的小区数']+wg['流量系数大于0.05小于0.2的小区数']+wg['流量系数0.2~0.5']+wg['流量系数0.5~1.5']+wg['流量系数1.5~3']+wg['流量系数3~5']+wg['流量系数>5'])

wg = wg[['总小区数','网格业务均衡比','日流量为0','流量系数大于0小于0.05的小区数','流量系数大于0.05小于0.2的小区数','流量系数0.2~0.5','流量系数0.5~1.5','流量系数1.5~3','流量系数3~5','流量系数>5']]
wg.to_csv('D:\guangdong\Result\wanggejunhengbi.csv',header=1,encoding='gbk') #保存列名存储