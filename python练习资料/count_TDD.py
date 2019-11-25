import pandas as pd
import numpy as np

# 计算现网有位置更新小区数
Address_LTE = pd.read_csv('D:\guangdong\Zcount\Addressupdate7.csv',encoding='gbk')
Address_LTE = Address_LTE.drop_duplicates('CGI')

# -找出Addressupdate7中CGI列在4G存量0127中存在，4G存量0127中筛选了网络制式为TDD和LTE；
Cl4Gcell  = pd.read_csv('D:\guangdong\Zcount\Cl4Gcell.csv',encoding='gbk')
Cl4Gcell = Cl4Gcell.drop_duplicates('CGI')
##############################################
Cl4Gcell_temp = Cl4Gcell
Cl4Gcell_FDD = Cl4Gcell.loc[Cl4Gcell['网络制式'].isin(['FDD'])]
###########################################
Cl4Gcell = Cl4Gcell.loc[Cl4Gcell['网络制式'].isin(['TDD','LTE'])]
tjb1 = Address_LTE.loc[(Address_LTE['CGI'].isin(Cl4Gcell['CGI']))]

tjb1F = Address_LTE.loc[(Address_LTE['CGI'].isin(Cl4Gcell_FDD['CGI']))]

###并入位置更新数
Tjb1 = pd.merge(Cl4Gcell,tjb1,on='CGI',how='inner')  # 匹配合并，交集

Tjb1F = pd.merge(Cl4Gcell_FDD,tjb1F,on='CGI',how='inner')  # 匹配合并，交集

##按地市统计tjb1中既有TAC数，又在综资的存量小区数 tbj2
cl_countcell = Tjb1.groupby('所属地市')['CGI'].count()
cl_countcell = cl_countcell.to_frame()
cl_countcell.columns = ['存量小区数']

Fcl_countcell = Tjb1F.groupby('所属地市')['CGI'].count()
Fcl_countcell = Fcl_countcell.to_frame()
Fcl_countcell.columns = ['存量小区数']

#找出Addressupdate7中CGI列在4G流程中0127中存在，4G流程中0127中筛选了网络制式为TDD和LTE；
Lcz4Gcell = pd.read_csv('D:\guangdong\Zcount\Lcz4Gcell.csv',encoding='gbk')
Lcz4Gcell = Lcz4Gcell.drop_duplicates('CGI')
Lcz4Gcell_FDD = Lcz4Gcell.loc[Lcz4Gcell['网络制式'].isin(['FDD'])]
Lcz4Gcell = Lcz4Gcell.loc[Lcz4Gcell['网络制式'].isin(['TDD','LTE'])]

#### 找出Addressupdate7中CGI列在4G流程中中存在,但不在存量中
tjb3_temp = Address_LTE.loc[(Address_LTE['CGI'].isin(Lcz4Gcell['CGI']))]
tjb3 = tjb3_temp.loc[(~tjb3_temp['CGI'].isin(Cl4Gcell['CGI']))]
#FDD
tjb3F_temp = Address_LTE.loc[(Address_LTE['CGI'].isin(Lcz4Gcell_FDD['CGI']))]
tjb3F = tjb3F_temp.loc[(~tjb3F_temp['CGI'].isin(Cl4Gcell_temp['CGI']))]

###并入位置更新数
tjb4 = pd.merge(Lcz4Gcell,tjb3,on='CGI',how='inner')  # 匹配合并，交集
#FDD
tjb4F = pd.merge(Lcz4Gcell_FDD,tjb3F,on='CGI',how='inner')  # 匹配合并，交集

##按地市统计tjb3中既有TAC数，又在综资的存量小区数 tbj4
lc_countcell = tjb4.groupby('所属地市')['CGI'].count()
lc_countcell = lc_countcell.to_frame()
lc_countcell.columns = ['流程小区数']

Flc_countcell = tjb4F.groupby('所属地市')['CGI'].count()
Flc_countcell = Flc_countcell.to_frame()
Flc_countcell.columns = ['流程小区数']

###存量小区数+流程小区数 =现网有位置更新小区数

#计算亿阳有性能
yiyang = pd.read_csv('D:\guangdong\Zcount\yiyang.csv',encoding='gbk')
yiyang = yiyang.drop_duplicates('CGI')
yiyang.rename(columns={'地市': '所属地市'},inplace=True)

yiyang_x = yiyang.loc[((yiyang['空口上行业务字节数']>=0)| (yiyang['空口下行业务字节数']>=0)) &
                      (yiyang['RRC连接建立成功次数']>=0) & (yiyang['E-RAB建立成功数']>=0)&
                      ((yiyang['网络制式'] == 'TDD')|(yiyang['网络制式'] == 'LTE'))]

yiyang_x_F = yiyang.loc[((yiyang['空口上行业务字节数']>=0)| (yiyang['空口下行业务字节数']>=0)) &
                      (yiyang['RRC连接建立成功次数']>=0) & (yiyang['E-RAB建立成功数']>=0) &
                        (yiyang['网络制式'] == 'FDD')]

tjb1_tem = tjb1[['CGI']]
tjb3_tem = tjb3[['CGI']]
tjb_temp = tjb1_tem.append(tjb3_tem)
yiyang_x = yiyang_x.loc[(yiyang_x['CGI'].isin(tjb_temp['CGI']))]

#FDD
tjb1F_tem = tjb1F[['CGI']]
tjb3F_tem = tjb3F[['CGI']]
tjbF_temp = tjb1F_tem.append(tjb3F_tem)
print(tjbF_temp.iloc[:,0].size)

yiyang_x_F = yiyang_x_F.loc[(yiyang_x_F['CGI'].isin(tjbF_temp['CGI']))]

#####
yiyang_x_countcell = yiyang_x.groupby('所属地市')['CGI'].count()
yiyang_x_countcell = yiyang_x_countcell.to_frame()
yiyang_x_countcell.columns = ['亿阳现网有性能小区数']
  #FDD
yiyangF_x_countcell = yiyang_x_F.groupby('所属地市')['CGI'].count()
yiyangF_x_countcell = yiyangF_x_countcell.to_frame()
yiyangF_x_countcell.columns = ['亿阳现网有性能小区数']

#计算亿阳采集小区数
yiyang_c = yiyang.loc[(yiyang['CGI'].isin(tjb_temp['CGI']))]
yiyang_countcell = yiyang_c.groupby('所属地市')['CGI'].count()
yiyang_countcell = yiyang_countcell.to_frame()
yiyang_countcell.columns = ['亿阳采集小区数']
  #FDD
yiyangF_c = yiyang.loc[(yiyang['CGI'].isin(tjbF_temp['CGI']))]
yiyangF_countcell = yiyangF_c.groupby('所属地市')['CGI'].count()
yiyangF_countcell = yiyangF_countcell.to_frame()
yiyangF_countcell.columns = ['亿阳采集小区数']

#大数据平台有采集完整数
dashuju = pd.read_csv('D:\guangdong\Zcount\dashuju.csv',encoding='gbk')
dashuju = dashuju.drop_duplicates('CGI')
dashuju_c = dashuju.loc[(dashuju['CGI'].isin(tjb_temp['CGI']))]
dashuju_countcell = dashuju_c.groupby('所属地市')['CGI'].count()
dashuju_countcell = dashuju_countcell.to_frame()
dashuju_countcell.columns = ['大数据采集小区数']
 #FDD
dashuju_c_F = dashuju.loc[(dashuju['CGI'].isin(tjbF_temp['CGI']))]
dashujuF_countcell = dashuju_c_F.groupby('所属地市')['CGI'].count()
dashujuF_countcell = dashujuF_countcell.to_frame()
dashujuF_countcell.columns = ['大数据采集小区数']

#计算大数据有性能
dashuju_x = dashuju.loc[((dashuju['上行流量(KByte)']>=0) | (dashuju['下行流量(KByte)']>=0))&
                        (dashuju['RRC连接建立成功次数']>=0) & (dashuju['E-RAB建立成功数']>=0)]

dashuju_x_T = dashuju_x.loc[(dashuju_x['CGI'].isin(tjb_temp['CGI']))]
dashuju_x_countcell = dashuju_x_T.groupby('所属地市')['CGI'].count()
dashuju_x_countcell = dashuju_x_countcell.to_frame()
dashuju_x_countcell.columns = ['大数据有性能小区数']
  #FDD
dashujuF_x = dashuju_x.loc[(dashuju_x['CGI'].isin(tjbF_temp['CGI']))]
dashujuF_x_countcell = dashujuF_x.groupby('所属地市')['CGI'].count()
dashujuF_x_countcell = dashujuF_x_countcell.to_frame()
dashujuF_x_countcell.columns = ['大数据有性能小区数']

# 计算资源可用率分子
xwqd = pd.read_csv('D:\guangdong\Zcount\Xqqd.csv',encoding='gbk')
xwqd = xwqd.drop_duplicates('CGI')
xwqd.rename(columns={'地市': '所属地市'},inplace=True)

xwqd = xwqd.loc[(xwqd['网络制式']!= '900') & (xwqd['网络制式']!= 'FDD') & (xwqd['网络制式']!= 'NB-IOT')
                &(xwqd['站点属性']!= '高铁')]
xwqd = xwqd.loc[(xwqd['CGI'].isin(Address_LTE['CGI']))]

xwqd = xwqd[['所属地市','有效时长']]

xwqd_counttime = xwqd .groupby('所属地市')['有效时长'].agg([np.sum])
xwqd_counttime.columns = ['总有效时长']

#计算资源可用率分母
souce = pd.read_csv('D:\guangdong\Zcount\souce.csv',encoding='gbk')
souce.rename(columns={'地市': '所属地市'},inplace=True)
souce = souce[['所属地市','LTE小区总时长','LTE资源可用率']]
souce  = souce .loc[~souce ['所属地市'].isin(['全省'])]

result = pd.merge(cl_countcell,lc_countcell,on='所属地市',how='outer',suffixes=('', '_y')) # pandas csv表左连接
result = pd.merge(result,yiyang_x_countcell,on='所属地市',how='outer',suffixes=('', '_y')) # pandas csv表左连接
result = pd.merge(result,yiyang_countcell,on='所属地市',how='outer',suffixes=('', '_y')) # pandas csv表左连接
result = pd.merge(result,dashuju_countcell,on='所属地市',how='outer',suffixes=('', '_y')) # pandas csv表左连接
result = pd.merge(result,dashuju_x_countcell,on='所属地市',how='outer',suffixes=('', '_y')) # pandas csv表左连接
result = pd.merge(result,xwqd_counttime,on='所属地市',how='outer',suffixes=('', '_y')) # pandas csv表左连接
result = pd.merge(result,souce,on='所属地市',how='outer',suffixes=('', '_y')) # pandas csv表左连接

result.set_index('所属地市',inplace= True)
result.fillna(0,inplace = True)
result.loc['全省'] = result.apply(lambda x: x.sum())
result['现网有位置更新小区数'] = result['存量小区数'] + result['流程小区数']
result['其中综资现网状小区比'] = result['存量小区数'] / result['现网有位置更新小区数']
result['其中综资工程态占比'] = result['流程小区数'] / result['现网有位置更新小区数']
result['亿阳现网有性能比例'] =  result['亿阳现网有性能小区数'] / result['现网有位置更新小区数']
result['亿阳采集完整率'] =  result['亿阳采集小区数'] / result['现网有位置更新小区数']
result['大数据平台有性能比例'] =  result['大数据有性能小区数'] / result['现网有位置更新小区数']
result['大数据平台完整率'] =  result['大数据采集小区数'] / result['现网有位置更新小区数']
result['实际资源可用率'] = result['总有效时长'] / result['LTE小区总时长']
result = result.reindex(['全省','广州','深圳','东莞','佛山','汕头','珠海','惠州','中山','江门','湛江','茂名','揭阳',
                         '韶关','河源','梅州','汕尾','阳江','肇庆','清远','潮州','云浮'])
print(result.info())
result.to_csv('D:\guangdong\Zcount\count_TDD.csv',header=1,encoding='gbk') #保存列名存储

result_F = pd.merge(Fcl_countcell,Flc_countcell,on='所属地市',how='outer',suffixes=('', '_y')) # pandas csv表左连接
result_F = pd.merge(result_F,yiyangF_x_countcell,on='所属地市',how='outer',suffixes=('', '_y')) # pandas csv表左连接
result_F = pd.merge(result_F,yiyangF_countcell,on='所属地市',how='outer',suffixes=('', '_y')) # pandas csv表左连接
result_F = pd.merge(result_F,dashujuF_countcell,on='所属地市',how='outer',suffixes=('', '_y')) # pandas csv表左连接
result_F = pd.merge(result_F,dashujuF_x_countcell,on='所属地市',how='outer',suffixes=('', '_y')) # pandas csv表左连接
# result_F.set_index('所属地市',inplace= True)
result_F.fillna(0,inplace = True)
result_F.loc['全省'] = result_F.apply(lambda x: x.sum())
result_F['现网有位置更新小区数'] = result_F['存量小区数'] + result_F['流程小区数']
result_F['其中综资现网状小区比'] = result_F['存量小区数'] / result_F['现网有位置更新小区数']
result_F['其中综资工程态占比'] = result_F['流程小区数'] / result_F['现网有位置更新小区数']
result_F['亿阳现网有性能比例'] = result_F['亿阳现网有性能小区数'] / result_F['现网有位置更新小区数']
result_F['亿阳采集完整率'] =  result_F['亿阳采集小区数'] / result_F['现网有位置更新小区数']
result_F['大数据平台有性能比例'] =  result_F['大数据有性能小区数'] /result_F['现网有位置更新小区数']
result_F['大数据平台完整率'] =  result_F['大数据采集小区数'] / result_F['现网有位置更新小区数']

result_F = result_F.reindex(['全省','广州','深圳','东莞','佛山','汕头','珠海','惠州','中山','江门','湛江','茂名','揭阳',
                         '韶关','河源','梅州','汕尾','阳江','肇庆','清远','潮州','云浮'])
result_F.to_csv('D:\guangdong\Zcount\count_FDD.csv',header=1,encoding='gbk') #保存列名存储