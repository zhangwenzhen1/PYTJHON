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
zb1 = zb1.groupby('地市')['日流量GB'].agg(np.mean)
zb1.columns = ['地市','单小区日均流量GB']
zb['单小区日均流量GB'] = zb['地市'].map(zb1)
zb['流量系数'] = zb['日流量GB']/zb['单小区日均流量GB']

# zb['制式标识'] =np.where(zb['制式标识']==1,'TDD',
#                      np.where(zb['制式标识']==2,'FDD',''))

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


# zb12 =zb[['小区名称','制式标识','载波带宽(MHZ)','带宽','NB','流量系数','流量系数1']]
# zb12.to_csv('D:\guangdong\Result\z2.csv', header=1, encoding='gbk')  # 保存列名存储
# Qinyuan = zb.loc[(zb['地市'] =='清远')]
print(zb.iloc[:,0].size)
zb.to_csv('D:\guangdong\Result\prov_coefficient.csv', header=1, encoding='gbk')  # 保存列名存储

def function1(zb):
    g1 = zb.loc[(zb['日流量GB'] == 0) & (zb['地市'].notnull()), ['地市', '小区ID', '流量系数']]
    g2 = zb.loc[(zb['流量系数'] > 0) & (zb['流量系数'] <= 0.05), ['地市', '小区ID', '流量系数']]
    g3 = zb.loc[(zb['流量系数'] > 0.05) & (zb['流量系数'] <= 0.2), ['地市', '小区ID', '流量系数']]
    g4 = zb.loc[(zb['流量系数'] > 0.2) & (zb['流量系数'] <= 0.5), ['地市', '小区ID', '流量系数']]
    g5 = zb.loc[(zb['流量系数'] > 0.5) & (zb['流量系数'] <= 1.5), ['地市', '小区ID', '流量系数']]
    g6 = zb.loc[(zb['流量系数'] > 1.5) & (zb['流量系数'] <= 3), ['地市', '小区ID', '流量系数']]
    g7 = zb.loc[(zb['流量系数'] > 3) & (zb['流量系数'] <= 5), ['地市', '小区ID', '流量系数']]
    g8 = zb.loc[(zb['流量系数'] > 5), ['地市', '小区ID', '流量系数']]

    g_1 = g1.groupby('地市')['小区ID'].count()
    g_2 = g2.groupby('地市')['小区ID'].count()
    g_3 = g3.groupby('地市')['小区ID'].count()
    g_4 = g4.groupby('地市')['小区ID'].count()
    g_5 = g5.groupby('地市')['小区ID'].count()
    g_6 = g6.groupby('地市')['小区ID'].count()
    g_7 = g7.groupby('地市')['小区ID'].count()
    g_8 = g8.groupby('地市')['小区ID'].count()
    # series转换成frame格式
    g_1 = g_1.to_frame()
    g_2 = g_2.to_frame()
    g_2.columns = ['流量系数大于0小于0.05的小区数']
    g_3 = g_3.to_frame()
    g_3.columns = ['流量系数大于0.05小于0.2的小区数']
    # print(g_3.head(30))
    g_4 = g_4.to_frame()
    g_5 = g_5.to_frame()
    g_6 = g_6.to_frame()
    g_7 = g_7.to_frame()
    g_8 = g_8.to_frame()
    gg = pd.merge(g_1, g_2, on='地市', how='right', suffixes=('', '_y'))
    gg = pd.merge(gg, g_3, on='地市', how='left', suffixes=('', '_y'))  # pandas csv表左连接
    gg = pd.merge(gg, g_4, on='地市', how='left', suffixes=('', '_q'))
    gg = pd.merge(gg, g_5, on='地市', how='left', suffixes=('', '_y'))
    gg = pd.merge(gg, g_6, on='地市', how='left', suffixes=('', '_y'))
    gg = pd.merge(gg, g_7, on='地市', how='left', suffixes=('', '_y'))
    gg = pd.merge(gg, g_8, on='地市', how='left', suffixes=('', '_y'))
    gg.columns = ['日流量为0', '流量系数大于0小于0.05的小区数', '流量系数大于0.05小于0.2的小区数', '流量系数0.2~0.5', '流量系数0.5~1.5',
                  '流量系数1.5~3', '流量系数3~5', '流量系数>5']
    gg.fillna(0, inplace=True)
    gg.loc['全省'] = gg.apply(lambda x: x.sum())
    gg['业务均衡比'] = (gg['流量系数0.2~0.5'] + gg['流量系数0.5~1.5'] + gg['流量系数1.5~3']) * 1.0 / (
            gg['日流量为0'] + gg['流量系数大于0小于0.05的小区数'] + gg['流量系数大于0.05小于0.2的小区数']
            + gg['流量系数0.2~0.5'] + gg['流量系数0.5~1.5'] + gg['流量系数1.5~3'] + gg['流量系数3~5'] + gg['流量系数>5'])
    # zb1 = zb1.to_frame()
    return gg

def function2(gg,zb1):
    zb1 = zb1.to_frame()
    ###此处日流量GB为各地市单小区日均流量
    gg = pd.merge(zb1, gg, on='地市', how='right', suffixes=('', '_y'))
    # 赋予全省日均流量值
    # print(gg.head(50))
    gg.iat[21, 0] = z_mean
    gg = gg.reindex(
        ['全省', '广州', '深圳', '东莞', '佛山', '汕头', '珠海', '惠州', '中山', '江门', '湛江', '茂名', '揭阳', '韶关', '河源', '梅州',
         '汕尾', '阳江', '肇庆', '清远', '潮州', '云浮'])
    gg = gg[['日流量GB', '业务均衡比', '日流量为0', '流量系数大于0小于0.05的小区数', '流量系数大于0.05小于0.2的小区数', '流量系数0.2~0.5',
             '流量系数0.5~1.5', '流量系数1.5~3', '流量系数3~5', '流量系数>5']]
    return gg
'''
#################################################################################
zb_temp1 = zb.loc[(zb['室内外基站属性']=='室内')]

zb_temp2 = zb.loc[(zb['室内外基站属性']=='室外宏站')|(zb['室内外基站属性']=='室外微站')]

zb_temp1 = function1(zb_temp1)
zb_temp1 = function2(zb_temp1,zb1)
zb_1 = function1(zb)
zb_1 =function2(zb_1,zb1)

zb_temp2 = function1(zb_temp2)
zb_temp2 = function2(zb_temp2,zb1)
######################
writer = pd.ExcelWriter('D:\guangdong\Result\zhoumangshi1203-1209.xlsx')
zb_1.to_excel(writer,'总表',)
zb_temp1.to_excel(writer,'室内',)
zb_temp2.to_excel(writer,'室外',)
writer.save()
#############################################################################################
'''

###################################################################################################
zb_FDD = zb.loc[(zb['制式标识']=='FDD')]
zb_TDD = zb.loc[(zb['制式标识']=='TDD')]

zb_1 = function1(zb)
zb_1 =function2(zb_1,zb1)

zb_FDD = function1(zb_FDD)
zb_FDD = function2(zb_FDD, zb1)

zb_TDD= function1(zb_TDD)
zb_TDD = function2(zb_TDD, zb1)
writer = pd.ExcelWriter('D:\guangdong\Result\zhoumangshi1210-1216.xlsx')
zb_1.to_excel(writer,'总表',)
zb_FDD.to_excel(writer,'FDD',)
zb_TDD.to_excel(writer,'TDD',)
writer.save()
############################################################
