import pandas as pd
import numpy as np

# gs_Totalparameters = pd.read_csv('D:\gxt\Highload\gs_totalparameters.csv',encoding='gbk')
# print(gs_Totalparameters.columns)
# gs_Totalparameters = gs_Totalparameters.loc[(gs_Totalparameters['基站经度'].notnull()) &
#                                             (gs_Totalparameters['基站纬度'].notnull()) &
#                                             (gs_Totalparameters['地市'].isin(['广州','深圳'])) &
#                                             (gs_Totalparameters['逻辑站站点类型']=='宏站'),
#                                             ['地市', '小区名称','CGI','PCI','基站名称','基站经度', '基站纬度','天线方向角',
#                                              '物理站经度', '物理站纬度','逻辑站站点类型','逻辑站区域类型']]
# gs_Totalparameters.to_csv('D:\gxt\Highload\Totalparameters.csv',header=1,encoding='gbk',index=False)


def f_avg(b):
    b = b.groupby(['地市','ECGI'],as_index = True)['日均流量(GB)','自忙时RRC连接最大数','自忙时上行利用率PUSCH','自忙时下行利用率PDSCH',
                                 '自忙时下行利用率PDCCH','自忙时峰值利用率'].agg([np.mean,np.max])
    b = b.reset_index(drop=False)
    return b

high_cell = pd.read_csv('D:\gxt\Highload\high_cell.csv',encoding='gbk')
# high_cell_gz = high_cell.loc[(high_cell['地市'] =='广州')]
# high_cell_sz = high_cell.loc[(high_cell['地市'] =='深圳')]
# print(len(high_cell_gz['CGI'].unique()))
# print(len(high_cell_sz['CGI'].unique()))
print(len(high_cell['CGI'].unique()))
cap = pd.read_csv('D:\gxt\Highload\capacity.csv',encoding='gbk')
cap = cap[['CGI','日均流量(GB)','自忙时RRC连接最大数','自忙时上行利用率PUSCH','自忙时下行利用率PDSCH','自忙时下行利用率PDCCH','自忙时峰值利用率']]
# print(cap.columns)
Result_sz = pd.read_csv('D:\gxt\Highload\Result_sz.csv',encoding='gbk')
print(len(Result_sz['ECGI'].unique()))
Result_sz= Result_sz.drop_duplicates()
# print(Result_sz.iloc[:,0].size)

Result_sz = Result_sz[['地市','ECGI','CGI']]
# print(Result_sz.iloc[:,0].size)

Result_gz = pd.read_csv('D:\gxt\Highload\Result_gz.csv',encoding='gbk')
print(len(Result_gz['ECGI'].unique()))
Result_gz= Result_gz.drop_duplicates()
# print(Result_gz.iloc[:,0].size)


Result_gz = Result_gz[['地市','ECGI','CGI']]
# print(Result_gz.iloc[:,0].size)

Result_sz = pd.merge(Result_sz,cap,on=['CGI'],how='left',suffixes=('', '_y'))

Result_gz = pd.merge(Result_gz,cap,on=['CGI'],how='left',suffixes=('', '_y'))

sz_result = f_avg(Result_sz)
gz_result = f_avg(Result_gz)

sz_result.to_csv('D:\gxt\Highload\sz_result.csv',header=1,encoding='gbk',index=False)
gz_result.to_csv('D:\gxt\Highload\gz_result.csv',header=1,encoding='gbk',index=False)