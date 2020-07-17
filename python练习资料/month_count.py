import pandas as pd
import numpy as np

df1 = pd.read_csv('D:\guangdong\zhoumangshi1203-1209.csv',encoding='gbk')

df2 = pd.read_csv('D:\guangdong\zhoumangshi1210-1216.csv',encoding='gbk')

df1 = df1.drop_duplicates('小区ID')
df2 = df2.drop_duplicates('小区ID')

# print(df.columns)

def f(x):
    return x.max()

def sel_col(a):
    a = a[['地市','小区ID','上行日流量(MB)','下行日流量(MB)','有效RRC连接平均数', '有效RRC连接最大数', 'RRC连接平均数',
           'RRC连接最大数','平均E-RAB数','VOLTE语音话务量', '下行PRB平均利用率(v2.8)', '上行PRB平均利用率(v2.8)', 'PDCCH信道CCE占用率']]
    a['无线利用率'] = a[['上行PRB平均利用率(v2.8)', '下行PRB平均利用率(v2.8)', 'PDCCH信道CCE占用率']].apply(f, axis=1)
    return a

def tras_num(c):
    c['上行日流量(MB)'] = c['上行日流量(MB)'].astype(np.float64)
    c['下行日流量(MB)'] = c['下行日流量(MB)'].astype(np.float64)
    c['无线利用率'] = c['无线利用率'].astype(np.float64)
    c['有效RRC连接平均数'] = c['有效RRC连接平均数'].astype(np.float64)
    c['RRC连接平均数'] = c['RRC连接平均数'].astype(np.float64)
    c['RRC连接最大数'] = c['RRC连接最大数'].astype(np.float64)
    c['平均E-RAB数'] = c['平均E-RAB数'].astype(np.float64)
    c['下行PRB平均利用率(v2.8)'] = c['下行PRB平均利用率(v2.8)'].astype(np.float64)
    c['上行PRB平均利用率(v2.8)'] = c['上行PRB平均利用率(v2.8)'].astype(np.float64)
    c['PDCCH信道CCE占用率'] = c['PDCCH信道CCE占用率'].astype(np.float64)
    return c


def city_count(b):
    b = b.groupby(['地市','月份'], as_index=True)['上行日流量(MB)', '下行日流量(MB)','无线利用率','有效RRC连接平均数', '有效RRC连接最大数',
                                         'RRC连接平均数', 'RRC连接最大数','平均E-RAB数','VOLTE语音话务量',
                                         '下行PRB平均利用率(v2.8)', '上行PRB平均利用率(v2.8)', 'PDCCH信道CCE占用率'].agg(np.mean)
    b = b.reset_index(drop=False)
    return b

#####场景统计
def scene_count(c,e):
    S = pd.merge(c,e,on='小区ID',how='inner')  # 匹配合并，交集
    S = S.groupby(['场景', '月份'], as_index=True)['上行日流量(MB)', '下行日流量(MB)', '无线利用率', '有效RRC连接平均数', '有效RRC连接最大数',
                                               'RRC连接平均数', 'RRC连接最大数', '平均E-RAB数', 'VOLTE语音话务量',
                                               '下行PRB平均利用率(v2.8)', '上行PRB平均利用率(v2.8)', 'PDCCH信道CCE占用率'].agg(np.mean)
    S = S.reset_index(drop=False)
    return S

zb1 = sel_col(df1)
zb2 = sel_col(df2)
zb = zb1.append(zb2)

num_f = tras_num(zb)
Reult = city_count(num_f)

writer = pd.ExcelWriter('D:\guangdong\Result\zhoumang_count.xlsx')
Reult.to_excel(writer,'地市级',index=False)

writer.save()




