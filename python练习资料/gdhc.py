import pandas as pd
import numpy as np
df1  = pd.read_csv('D:\Volte.m_mrs_packetlrdlq_yunf.csv',encoding='utf-8')
df2  = pd.read_csv('D:\Volte.m_mrs_packetlrulq_yunf.csv',encoding='utf-8')
df1['gtz'] = df1['packetlossratedlq_17']+df1['packetlossratedlq_18']+df1['packetlossratedlq_19']+df1['packetlossratedlq_20']\
             +df1['packetlossratedlq_21']+df1['packetlossratedlq_22']+df1['packetlossratedlq_23']+df1['packetlossratedlq_24']\
             +df1['packetlossratedlq_25']+df1['packetlossratedlq_26']+df1['packetlossratedlq_27']
df2 ['gtz'] = df2['packetlossrateulq_17']+df2['packetlossrateulq_18']+df2['packetlossrateulq_19']+df2['packetlossrateulq_20']\
             +df2['packetlossrateulq_21']+df2['packetlossrateulq_22']+df2['packetlossrateulq_23']+df2['packetlossrateulq_24']\
             +df2['packetlossrateulq_25']+df2['packetlossrateulq_26']+df2['packetlossrateulq_27']

df1['dt'] = df1['packetlossratedlq_26']+df1['packetlossratedlq_27']
df2['dt'] = df2['packetlossrateulq_26']+df2['packetlossrateulq_27']
print(df2.columns)
def function1(a):
    a = a.groupby(['cgi'])['gtz','dt','packetlrdlq_count', 'packetlrdlq_sum'
    ].agg(np.mean)
    a = a.reset_index(drop=False)
    return a

def function2(a):
    a = a.groupby(['cgi'])['gtz','dt','packetlrulq_count', 'packetlrulq_sum'].agg(np.mean)
    a = a.reset_index(drop=False)
    return a

df_1 = function1(df1)
df_2 =function2(df2)
print(df_2.columns)
df_1['gdb'] =df_1['packetlrdlq_sum']*1.0/df_1['packetlrdlq_count']
df_2['gdb'] =df_2['packetlrulq_sum']*1.0/df_2['packetlrulq_count']
df_1 = df_1.loc[df_1['packetlrdlq_count']>500]
df_2 = df_2.loc[df_2['packetlrulq_count']>500]
df_2.to_csv('D:\GDresult\df_2.csv',header=1,encoding='gbk',index=False) #保存列名存储
df_1.to_csv('D:\GDresult\df_1.csv',header=1,encoding='gbk',index=False) #保存列名存储