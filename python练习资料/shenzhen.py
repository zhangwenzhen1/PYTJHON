import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

shenzhen_1 = pd.read_csv('D:\shenzhen\sz_hw_1.csv',encoding='gbk')
shenzhen_2 = pd.read_csv('D:\shenzhen\sz_hw_2.csv',encoding='gbk')
shenzhen_CGI = pd.read_csv('D:\shenzhen\szcgi.csv',encoding='gbk')
shenzhen = shenzhen_1.append(shenzhen_2)
shenzhen = shenzhen.drop_duplicates()

shenzhen = shenzhen.loc[(~shenzhen['CGI'].isin(shenzhen_CGI['CGI']))]
shenzhen = shenzhen.loc[(shenzhen['上行流量（GB)'].notnull()) &(shenzhen['上行流量（GB)']!=0) &(shenzhen['上行流量（GB)']!='NIL')
                        &(shenzhen['小区RB上行平均干扰电平(dBm)']!='NIL') &(shenzhen['E-RAB流量(KB)']!='/0')
                        &(shenzhen['上行利用率(%)']!='NIL') &(shenzhen['下行利用率(%)']!='NIL')&(shenzhen['上行利用率(%)']!='/0')
                        &(shenzhen['下行利用率(%)']!='/0')&(shenzhen['RRC有效平均连接用户数（个）']!='NIL') &(shenzhen['RRC有效平均连接用户数（个）']!='/0')
                        &(shenzhen['用户面平均上行速率(Mbps)']!='NIL') &(shenzhen['用户面平均上行速率(Mbps)']!='/0')
                        &(shenzhen['用户面平均上行时延(ms)']!='NIL') &(shenzhen['用户面平均上行时延(ms)']!='/0')
                        &(shenzhen['用户面平均下行速率(Mbps)']!='NIL') &(shenzhen['用户面平均下行速率(Mbps)']!='/0')
                        &(shenzhen['用户面平均下行时延(ms)']!='NIL') &(shenzhen['用户面平均下行时延(ms)']!='/0')
                        &(shenzhen['下行流量（GB)'].notnull()) &(shenzhen['下行流量（GB)']!=0) &(shenzhen['下行流量（GB)']!='NIL')]

shenzhen['上行流量（GB)'] = shenzhen['上行流量（GB)'].astype(np.float64)
shenzhen['下行流量（GB)'] = shenzhen['下行流量（GB)'].astype(np.float64)
shenzhen  = shenzhen.loc[(shenzhen['小区带宽']=='CELL_BW_N75') | (shenzhen['小区带宽']=='CELL_BW_N100')]
shenzhen['小区RB上行平均干扰电平(dBm)'] = shenzhen['小区RB上行平均干扰电平(dBm)'].astype(np.float64)

shenzhen['E-RAB流量(KB)'] = shenzhen['E-RAB流量(KB)'].astype(np.float64)
shenzhen['包分类'] =np.where(shenzhen['E-RAB流量(KB)'] >= 1000,'大包',
                          np.where(((shenzhen['E-RAB流量(KB)'] >= 300 )& (shenzhen['E-RAB流量(KB)'] < 1000)),'中包','小包'))
shenzhen['上行利用率(%)'] = shenzhen['上行利用率(%)'].astype(np.float64)
shenzhen['下行利用率(%)'] = shenzhen['下行利用率(%)'].astype(np.float64)
shenzhen = shenzhen.loc[(shenzhen['上行利用率(%)'] < 100) & (shenzhen['下行利用率(%)'] < 100)]
shenzhen['上行利用率(%)'] = shenzhen['上行利用率(%)'].apply(np.round)

shenzhen['下行利用率(%)'] = shenzhen['下行利用率(%)'].apply(np.round)
shenzhen['RRC有效平均连接用户数（个）'] = shenzhen['RRC有效平均连接用户数（个）'].astype(np.float64)
shenzhen['用户面平均上行速率(Mbps)'] = shenzhen['用户面平均上行速率(Mbps)'].astype(np.float64)
shenzhen['用户面平均上行时延(ms)'] = shenzhen['用户面平均上行时延(ms)'].astype(np.float64)
shenzhen['用户面平均下行速率(Mbps)'] = shenzhen['用户面平均下行速率(Mbps)'].astype(np.float64)
shenzhen['用户面平均下行时延(ms)'] = shenzhen['用户面平均下行时延(ms)'].astype(np.float64)

print(shenzhen.iloc[:,0].size)

shenzhen_FDD = shenzhen.loc[(shenzhen['网络制式'] == 'CELL_FDD')]
shenzhen_TDD = shenzhen.loc[(shenzhen['网络制式'] == 'CELL_TDD')]

def function1(a):
    a = a.groupby(['上行利用率(%)','包分类'])[
        '用户面平均上行速率(Mbps)', '上行流量（GB)', 'RRC有效平均连接用户数（个）', '用户面平均上行时延(ms)','小区RB上行平均干扰电平(dBm)'].agg([len, np.mean])
    a = a.reset_index(drop=False)
    return a

def function2(b):
    b = b.groupby(['下行利用率(%)','包分类'])[
        '用户面平均下行速率(Mbps)', '下行流量（GB)', 'RRC有效平均连接用户数（个）', '用户面平均下行时延(ms)'].agg([len, np.mean])
    b = b.reset_index(drop=False)
    return b
def function3(a,b):
    c = pd.merge(a, b, on=['上行利用率(%)','包分类'], how='left',suffixes=('_T', '_F'))  # pandas csv表左连接
    return c

def function4(a,b):
    c = pd.merge(a, b, on=['下行利用率(%)','包分类'], how='left',suffixes=('_T', '_F'))  # pandas csv表左连接
    return c

shenzhen_F1 = function1(shenzhen_FDD)
shenzhen_T1 = function1(shenzhen_TDD)
# shenzhen_TF1 = function3(shenzhen_T1,shenzhen_F1)
shenzhen_T1.to_csv('D:\shenzhen\Result\sz_hw_TDD_U.csv',header=1,encoding='gbk',index=False) #保存列名存储
shenzhen_F1.to_csv('D:\shenzhen\Result\sz_hw_FDD_U.csv',header=1,encoding='gbk',index=False) #保存列名存储
shenzhen_F2 = function2(shenzhen_FDD)
shenzhen_T2 = function2(shenzhen_TDD)
# shenzhen_TF2 = function4(shenzhen_T2,shenzhen_F2)
shenzhen_T2.to_csv('D:\shenzhen\Result\sz_hw_TDD_D.csv',header=1,encoding='gbk',index=False) #保存列名存储
shenzhen_F2.to_csv('D:\shenzhen\Result\sz_hw_FDD_D.csv',header=1,encoding='gbk',index=False) #保存列名存储
# print(shenzhen.iloc[:,0].size)

guangzhouA = pd.read_csv('D:\shenzhen\guangzhouA.csv',encoding='gbk')
print(guangzhouA.columns)
guangzhouA = guangzhouA.loc[(guangzhouA['上行流量（GB)'].notnull()) &(guangzhouA['上行流量（GB)']!=0)
                            &(guangzhouA['下行流量（GB)'].notnull()) &(guangzhouA['下行流量（GB)']!=0)
                            &(guangzhouA['上行利用率(%)'].notnull()) &(guangzhouA['上行利用率(%)']!=0)
                            &(guangzhouA['下行利用率(%)'].notnull()) &(guangzhouA['下行利用率(%)']!=0)
                            &(guangzhouA['RRC有效平均连接用户数（个）'].notnull()) &(guangzhouA['RRC有效平均连接用户数（个）']!=0)
                            &(guangzhouA['用户面平均上行速率(Mbps)'].notnull()) &(guangzhouA['用户面平均上行速率(Mbps)']!=0)
                            &(guangzhouA['用户面平均下行速率(Mbps)'].notnull()) &(guangzhouA['用户面平均下行速率(Mbps)']!=0)
                            &(guangzhouA['用户面平均下行时延(ms)'].notnull())&(guangzhouA['E-RAB流量(KB)'].notnull())
                            &(guangzhouA['小区RB上行平均干扰电平(dBm)'].notnull())]
guangzhouA  = guangzhouA.loc[(guangzhouA['小区带宽']==15) | (guangzhouA['小区带宽']==20)]

print(guangzhouA.info())
guangzhouA['包分类'] =np.where(guangzhouA['E-RAB流量(KB)'] >= 1000,'大包',
                           np.where(((guangzhouA['E-RAB流量(KB)'] >= 300 )& (guangzhouA['E-RAB流量(KB)'] < 1000)),'中包','小包'))

guangzhouA = guangzhouA.loc[(guangzhouA['上行利用率(%)'] < 100) & (guangzhouA['下行利用率(%)'] < 100)]

guangzhouA['上行利用率(%)'] = guangzhouA['上行利用率(%)'].apply(np.round)
guangzhouA['下行利用率(%)'] = guangzhouA['下行利用率(%)'].apply(np.round)

guangzhouA_FDD = guangzhouA.loc[(guangzhouA['网络制式'] == 'FDD')]
guangzhouA_TDD = guangzhouA.loc[(guangzhouA['网络制式'] == 'TDD')]

def function11(a):
    a = a.groupby(['上行利用率(%)','包分类'])[
        '用户面平均上行速率(Mbps)', '上行流量（GB)', 'RRC有效平均连接用户数（个）','小区RB上行平均干扰电平(dBm)'].agg([len, np.mean])
    a = a.reset_index(drop=False)
    return a

def function22(b):
    b = b.groupby(['下行利用率(%)','包分类'])[
        '用户面平均下行速率(Mbps)', '下行流量（GB)', 'RRC有效平均连接用户数（个）', '用户面平均下行时延(ms)'].agg([len, np.mean])
    b = b.reset_index(drop=False)
    return b
def function33(a,b):
    c = pd.merge(a, b, on=['上行利用率(%)','包分类'], how='left',suffixes=('_T', '_F'))  # pandas csv表左连接
    return c

def function44(a,b):
    c = pd.merge(a, b, on=['下行利用率(%)','包分类'], how='left',suffixes=('_T', '_F'))  # pandas csv表左连接
    return c

guangzhouA_F1 = function11(guangzhouA_FDD)
guangzhouA_T1 = function11(guangzhouA_TDD)
# guangzhouA_TF1 = function33(guangzhouA_T1,guangzhouA_F1)
guangzhouA_T1.to_csv('D:\shenzhen\Result\gz_A_TDD_U.csv',header=1,encoding='gbk',index=False) #保存列名存储
guangzhouA_F1.to_csv('D:\shenzhen\Result\gz_A_FDD_U.csv',header=1,encoding='gbk',index=False) #保存列名存储
guangzhouA_F2 = function22(guangzhouA_FDD)
guangzhouA_T2 = function22(guangzhouA_TDD)
# guangzhouA_TF2 = function44(guangzhouA_T2,guangzhouA_F2)
guangzhouA_T2.to_csv('D:\shenzhen\Result\gz_A_TDD_D.csv',header=1,encoding='gbk',index=False) #保存列名存储
guangzhouA_F2.to_csv('D:\shenzhen\Result\gz_A_FDD_D.csv',header=1,encoding='gbk',index=False) #保存列名存储




