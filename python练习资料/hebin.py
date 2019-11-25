import numpy as np
import pandas as pd
from pandas import Series, DataFrame

#读表
CIO3 = pd.read_csv('D:\guangdong\Fenxishuju\CIO_3.csv',encoding='gbk')
CIO4 = pd.read_csv('D:\guangdong\Fenxishuju\CIO_4.csv',encoding='utf-8')
LINQUDUI3 = pd.read_csv('D:\guangdong\Fenxishuju\LINQUDUI_3.csv',encoding='gbk')
LINQUDUI4 = pd.read_csv('D:\guangdong\Fenxishuju\LINQUDUI_4.csv',encoding='gbk')
MENXIAN3 = pd.read_csv('D:\guangdong\Fenxishuju\MENXIAN_3.csv',encoding='utf-8')
MENXIAN4 = pd.read_csv('D:\guangdong\Fenxishuju\MENXIAN_4.csv',encoding='utf-8')
MENXIAN2_3 = pd.read_csv('D:\guangdong\Fenxishuju\MENXIAN2_3.csv',encoding='utf-8')
MENXIAN2_4 = pd.read_csv('D:\guangdong\Fenxishuju\MENXIAN2_4.csv',encoding='utf-8')
Zhuanhuan = pd.read_csv('D:\guangdong\Fenxishuju\CIOchange.csv',encoding='gbk')
Zhuanhuan = Zhuanhuan.groupby('LNREL_CION_3',)['CIO'].agg(np.mean)
#
CIO = CIO3.append(CIO4)
CIO = CIO.drop_duplicates()

CIO['CGI'] = CIO['ENBID'].map(str)+'-'+CIO['CELL_ID'].map(str)
CIO['cio'] = CIO['LNREL_CION_3'].map(Zhuanhuan)

##选出LNREL_ECGI_ADJ_ENB_ID或LNREL_ECGI_LCR_ID不为空的列
CIO_temp = CIO.loc[(CIO['LNREL_ECGI_ADJ_ENB_ID'].notnull()|CIO['LNREL_ECGI_LCR_ID'].notnull())]
##选出LNREL_ECGI_ADJ_ENB_ID或LNREL_ECGI_LCR_ID为空的列
CIO_temp1 = CIO.loc[(CIO['LNREL_ECGI_ADJ_ENB_ID'].isnull()|CIO['LNREL_ECGI_LCR_ID'].isnull())]
CIO_temp1['linquCGI'] = ''

CIO_temp['LNREL_ECGI_ADJ_ENB_ID'] = CIO_temp['LNREL_ECGI_ADJ_ENB_ID'].astype(np.uint64)
CIO_temp['LNREL_ECGI_LCR_ID'] = CIO_temp['LNREL_ECGI_LCR_ID'].astype(np.uint64)
CIO_temp['linquCGI'] = CIO_temp['LNREL_ECGI_ADJ_ENB_ID'].map(str)+'-'+CIO_temp['LNREL_ECGI_LCR_ID'].map(str)
CIO = CIO_temp.append(CIO_temp1)
# #
LINQUDUI = LINQUDUI3.append(LINQUDUI4)
LINQUDUI = LINQUDUI.drop_duplicates()

#
MENXIAN = MENXIAN3.append(MENXIAN4)
MENXIAN  = LINQUDUI.drop_duplicates()
#
MENXIAN2 = MENXIAN2_3.append(MENXIAN2_4)
MENXIAN2  = MENXIAN2.drop_duplicates()

#
CIO.to_csv('D:\guangdong\Fenxishuju\HebingCIO.csv',header=1,encoding='utf-8',index=False)
LINQUDUI.to_csv('D:\guangdong\Fenxishuju\HebingLINQUDUI.csv',header=1,encoding='utf-8',index=False)
MENXIAN.to_csv('D:\guangdong\Fenxishuju\HebingMENXIAN.csv',header=1,encoding='utf-8',index=False)
MENXIAN2.to_csv('D:\guangdong\Fenxishuju\HebingMENXIAN2.csv',header=1,encoding='utf-8',index=False)




