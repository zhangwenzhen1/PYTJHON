import pandas as pd
import numpy as np

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
def xiuzheng(x):
    if np.isnan(x):
        return x
    else:
        x = 0
        return x
def function(a,b):
    df3 = pd.merge(a,b,left_on='CGI',right_on='cgi',how='left',suffixes=('', '_y')) # pandas csv表左连接
    df3 = df3.drop_duplicates()
    df3.drop( axis =1, columns= ['starttime_date', 'cgi', 'city', 'cell_name'],inplace=True)
    df3 = df3[['日期', '省份', '景区名称', '景区编号ID', '小区名称', 'CGI','mr覆盖率','日均流量gb','上行prb平均利用率','上行峰值流量mb',
              '下行prb平均利用率','下行峰值流量mb', 'pdcch信道cce占用率', '有效rrc连接最大数',
           '无线接通率', '无线掉线率', 'volte无线接通率', 'volte无线掉话率', 'srvcc切换成功率']]
    df3.columns = ['日期', '省份', '景区名称', '景区编号ID', '小区名称', 'CGI','MR覆盖率','日均4G流量(GB)','日峰值上行利用率',
                   '上行利用率峰值时段流量(上行流量MB)','日峰值下行利用率','下行利用率峰值时段流量(下行流量MB)','PDCCH信道CCE日峰值利用率',
                   '有效RRC连接最大数(个)','无线接通率','无线掉线率','volte无线接通率','volte无线掉话率','Srvcc切换成功率']
    # df3.apply(pd.to_numeric, errors='ignore')

    df3_temp1 = df3.loc[(df3['日均4G流量(GB)'].notnull()) & (df3['日均4G流量(GB)']!=0)]

    df3_temp2 = df3.loc[(df3['日均4G流量(GB)'] == 0)]

    df3_temp3 = df3.loc[(df3['日均4G流量(GB)'].isnull())]


    df3_temp1['无线接通率'].fillna(100, inplace=True)
    df3_temp1['无线掉线率'].fillna(0, inplace=True)
    df3_temp1['volte无线接通率'].fillna(100, inplace=True)
    df3_temp1['volte无线掉话率'].fillna(0, inplace=True)
    df3_temp1['Srvcc切换成功率'].fillna(100, inplace=True)

    df3_temp2['日峰值上行利用率'] = df3_temp2['日峰值上行利用率'].apply(lambda x: xiuzheng(x))
    df3_temp2['上行利用率峰值时段流量(上行流量MB)'] = df3_temp2['上行利用率峰值时段流量(上行流量MB)'].apply(lambda x: xiuzheng(x))
    df3_temp2['日峰值下行利用率'] = df3_temp2['日峰值下行利用率'].apply(lambda x: xiuzheng(x))
    df3_temp2['下行利用率峰值时段流量(下行流量MB)'] = df3_temp2['下行利用率峰值时段流量(下行流量MB)'].apply(lambda x: xiuzheng(x))
    df3_temp2['PDCCH信道CCE日峰值利用率'] = df3_temp2['PDCCH信道CCE日峰值利用率'].apply(lambda x: xiuzheng(x))

    df3 = df3_temp1.append(df3_temp2)
    df3 = df3.append(df3_temp3)

    df3['日峰值上行利用率'] = df3['日峰值上行利用率'].apply(lambda x: tras(x))
    df3['日峰值下行利用率'] = df3['日峰值下行利用率'].apply(lambda x: tras(x))
    df3['PDCCH信道CCE日峰值利用率'] = df3['PDCCH信道CCE日峰值利用率'].apply(lambda x: tras(x))
    df3['无线接通率'] = df3['无线接通率'].apply(lambda x: tras(x))
    df3['无线掉线率'] = df3['无线掉线率'].apply(lambda x: tras(x))
    df3['volte无线接通率'] = df3['volte无线接通率'].apply(lambda x: tras(x))
    df3['volte无线掉话率'] = df3['volte无线掉话率'].apply(lambda x: tras(x))
    df3['Srvcc切换成功率'] = df3['Srvcc切换成功率'].apply(lambda x: tras(x))
    df3['是否高负荷待扩容小区'] = df3[['日峰值上行利用率', '日峰值下行利用率', 'PDCCH信道CCE日峰值利用率']].apply(f, axis=1)

    # df3['MR覆盖率'] = df3['MR覆盖率'].apply(lambda x: format(x, '.1%'))
    # df3 = df3.drop_duplicates('CGI')
    return df3

writer = pd.ExcelWriter('D:\guangdong\Rongliang\jingquzhoubao.xlsx')
df = pd.read_csv('D:\guangdong\Rongliang\Fengjingqu.csv',encoding='gbk')
df1 = pd.read_csv('D:\guangdong\Rongliang\weekend_1006.csv',encoding='gbk')
df2 = pd.read_csv('D:\guangdong\Rongliang\weekend_1007.csv',encoding='gbk')
df_temp = function(df,df1)
df_temp['日期'] ='10月6日'
df_temp.to_excel(writer,'10月6日',index=False)
df_temp1 = function(df,df2)
df_temp1['日期'] ='10月7日'
df_temp1.to_excel(writer,'10月7日',index=False)
writer.save()

# for i in range(6):
#     All[i].to_excel(writer,sheet_name='sheet'+str(i))
# writer.save()


