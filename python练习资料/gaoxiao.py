import pandas as pd
import numpy as np
df = pd.read_csv('D:\guangdong\gaoxiaoqd.csv',encoding='gbk')
df1 = pd.read_csv('D:\guangdong\Fugai.csv',encoding='gbk')
df2 = pd.read_csv('D:\guangdong\gaoxiao_0824.csv',encoding='utf-8')
df1 = df1.loc[(df1['(移动)总采样点数'] > 0), ['CGI','(移动)弱覆盖采样点数量(小于-110)','(移动)总采样点数']]
df1['MR覆盖率'] = 1-df1['(移动)弱覆盖采样点数量(小于-110)']*1.0/df1['(移动)总采样点数']
df_temp1 = pd.merge(df2,df1,left_on='cgi',right_on='CGI',how='left',suffixes=('', '_y')) # pandas csv表左连接
print(df_temp1.columns)
def tras(x):
    x = x*0.01
    if x > 1:
        x = 0.993
    return x

def f(x):

    if x.max() > 0.5:
        return '是'
    if  np.isnan(x.max()):
        return ''
    else:
        return '否'

def function(a,b):
    df3 = pd.merge(a,b,left_on='CGI',right_on='cgi',how='left',suffixes=('', '_y')) # pandas csv表左连接
    df3.drop( axis =1, columns= ['starttime_date', 'cgi', 'city', 'cell_name'],inplace=True)
    df3 = df3[['地市', '小区中文名','CGI','场景','场景具体名称','MR覆盖率','日均流量gb','上行prb平均利用率','上行峰值流量mb',
              '下行prb平均利用率','下行峰值流量mb', 'pdcch信道cce占用率', '有效rrc连接最大数',
           '无线接通率', '无线掉线率', 'volte无线接通率', 'volte无线掉话率', 'srvcc切换成功率']]
    df3.columns = ['地市', '小区中文名','CGI','场景','场景具体名称','MR覆盖率','日均4G流量(GB)','日峰值上行利用率',
                   '上行利用率峰值时段流量(上行流量MB)','日峰值下行利用率','下行利用率峰值时段流量(下行流量MB)','PDCCH信道CCE日峰值利用率',
                   '有效RRC连接最大数(个)','无线接通率','无线掉线率','volte无线接通率','volte无线掉话率','Srvcc切换成功率']
    # df3.apply(pd.to_numeric, errors='ignore')
    df3['日峰值上行利用率'] = df3['日峰值上行利用率'].apply(lambda x: tras(x))
    df3['日峰值下行利用率'] = df3['日峰值下行利用率'].apply(lambda x: tras(x))
    df3['PDCCH信道CCE日峰值利用率'] = df3['PDCCH信道CCE日峰值利用率'].apply(lambda x: tras(x))
    df3['无线接通率'] = df3['无线接通率'].apply(lambda x: tras(x))
    df3['无线掉线率'] = df3['无线掉线率'].apply(lambda x: tras(x))
    df3['volte无线接通率'] = df3['volte无线接通率'].apply(lambda x: tras(x))
    df3['Srvcc切换成功率'] = df3['Srvcc切换成功率'].apply(lambda x: tras(x))
    df3['是否高负荷待扩容小区'] = df3[['日峰值上行利用率', '日峰值下行利用率', 'PDCCH信道CCE日峰值利用率']].apply(f, axis=1)
    df3['MR覆盖率'] = df3['MR覆盖率'].astype(np.float64)
    # df3['MR覆盖率'] = df3['MR覆盖率'].apply(lambda x: format(x, '.1%'))
    return df3

writer = pd.ExcelWriter('D:\guangdong\gaoxiaozhoubao.xlsx')

df_temp = function(df,df_temp1)
df_temp.to_excel(writer,'高校',index=False)

writer.save()