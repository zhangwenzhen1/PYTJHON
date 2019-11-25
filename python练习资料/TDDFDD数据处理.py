import numpy as np
import pandas as pd

def f(x):
    return x.max()
######
def function(a):
    a['最大利用率'] = a[['上行利用率(%)', '下行利用率(%)', 'CCE利用率(%)']].apply(f,axis =1)
    b = a.groupby(['CGI'])['最大利用率'].max()
    b = b.reset_index(drop=False)
    c =pd.merge(b,a,on=['CGI','最大利用率',],how='left',suffixes=('', '_y')) # pandas csv表左连接
    c = c.drop_duplicates('CGI')
    return c
#
def f_vag(a):
    a = a.groupby(['CGI'])['上行流量（GB)', '下行流量（GB)', '上行利用率(%)', '下行利用率(%)', 'CCE利用率(%)',
                           'RRC有效平均连接用户数（个）', '用户面平均上行速率(Mbps)', '用户面平均下行速率(Mbps)',
                           '用户面平均下行时延(ms)', 'E-RAB流量(KB)', '小区RB上行平均干扰电平(dBm)','最大利用率'].agg(np.mean)
    a = a.reset_index(drop=False)
    return a
#
TDD1031 = pd.read_csv('D:\gxt\FDD\TDD1031.csv',encoding='gbk')
TDD1101 = pd.read_csv('D:\gxt\FDD\TDD1101.csv',encoding='gbk')
TDD1102 = pd.read_csv('D:\gxt\FDD\TDD1102.csv',encoding='gbk')
TDD1103 = pd.read_csv('D:\gxt\FDD\TDD1103.csv',encoding='gbk')
TDD1104 = pd.read_csv('D:\gxt\FDD\TDD1104.csv',encoding='gbk')
TDD1105 = pd.read_csv('D:\gxt\FDD\TDD1105.csv',encoding='gbk')
TDD1106 = pd.read_csv('D:\gxt\FDD\TDD1106.csv',encoding='gbk')

Result_1 = function(TDD1031)
print(Result_1.columns)
Result_2 = function(TDD1101)
Result_3 = function(TDD1102)
Result_4 = function(TDD1103)
Result_5 = function(TDD1104)
Result_6 = function(TDD1105)
Result_7 = function(TDD1106)

result =Result_1.append(Result_1).append(Result_2).append(Result_3).append(Result_4).append(Result_5).append(Result_6).append(Result_7)
result = result[['CGI','上行流量（GB)', '下行流量（GB)', '上行利用率(%)', '下行利用率(%)', 'CCE利用率(%)',
                 'RRC有效平均连接用户数（个）', '用户面平均上行速率(Mbps)', '用户面平均下行速率(Mbps)',
                 '用户面平均下行时延(ms)', 'E-RAB流量(KB)', '小区RB上行平均干扰电平(dBm)','最大利用率']]
print(result.info())
Result = f_vag(result)
Result.to_csv('D:\gxt\FDD\Result2.csv',header=1,encoding='gbk',)

def function(a):
    a['最大利用率'] = a[['上行利用率(%)', '下行利用率(%)', 'CCE利用率(%)']].apply(f,axis =1)
    b = a.groupby(['day','CGI'])['最大利用率'].max()
    b = b.reset_index(drop=False)
    c =pd.merge(b,a,on=['day','CGI','最大利用率',],how='left',suffixes=('', '_y')) # pandas csv表左连接
    c = c.drop_duplicates('CGI')
    return c

TDD1 = pd.read_csv('D:\gxt\FDD\A_1031_1102.csv',encoding='gbk')
TDD2 = pd.read_csv('D:\gxt\FDD\A_1103_1104.csv',encoding='gbk')
TDD3 = pd.read_csv('D:\gxt\FDD\A_1105_1106.csv',encoding='gbk')

TDD = TDD1.append(TDD1).append(TDD2).append(TDD3)
print(TDD.columns)
TDD['取数时间'] = TDD['时间'].astype(np.str)
split2 = pd.DataFrame((x.split() for x in TDD['时间']),index=TDD.index,columns=['day','hour'])
TDD = pd.merge(TDD,split2,right_index=True, left_index=True,suffixes=('', '_y'))
# print(split2.head())
TDD = TDD.loc[(TDD['小区RB上行平均干扰电平(dBm)'].notnull())&(TDD['CGI']!='无数据')&(TDD['上行利用率(%)'].notnull())&
              (TDD['下行利用率(%)'].notnull())&(TDD['CCE利用率(%)'].notnull())]
print(TDD.info())
TDD = function(TDD)
TDD = TDD[['CGI','上行流量（GB)', '下行流量（GB)', '上行利用率(%)', '下行利用率(%)', 'CCE利用率(%)',
                 'RRC有效平均连接用户数（个）', '用户面平均上行速率(Mbps)', '用户面平均下行速率(Mbps)',
                 '用户面平均下行时延(ms)', 'E-RAB流量(KB)', '小区RB上行平均干扰电平(dBm)','最大利用率']]
print(TDD.info())
Result_A = f_vag(TDD)
Result_A.to_csv('D:\gxt\FDD\Result_A.csv',header=1,encoding='gbk',)