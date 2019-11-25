import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib
# fig = plt.figure()
# ax1 = fig.add_subplot(2,2,1)
# ax2 = fig.add_subplot(2,2,2)
# ax3 = fig.add_subplot(2,2,3)
# # 显示中文
# font1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simkai.ttf')# 显示中文
# plt.plot(np.random.randn(50).cumsum(),color ='k',linestyle='dashed',marker ='o')
# ax1.hist(np.random.randn(100),bins=20,color ='r',alpha =1)
# ax2.scatter(np.arange(30),np.arange(30)+3*np.random.randn(30))
# ax4 = fig.add_subplot(2,2,4)
# data =np.random.randn(30).cumsum()
# plt.plot(data,color ='g',label='故1')
# plt.plot(data,'k--',drawstyle='steps-post',label='设及')
# # fig,axes =plt.subplots(2,3)
#
# plt.legend(loc='best',prop=font1)# 显示中文
# plt.show()
# sz_1 = pd.read_csv('D:\shenzhen\sz_FDD-46.csv',encoding='gbk')
# sz_2 = pd.read_csv('D:\shenzhen\shenzhen_1.csv',encoding='gbk')
# sz_2 = sz_2.loc[(sz_2['上行流量（GB)']!= '0') & (sz_2['小区RB上行平均干扰电平(dBm)']!='NIL') & (sz_2['上行利用率(%)']!='NIL')
#                 &(sz_2['E-RAB流量(KB)']!= '/0')]
#
# sz_2['上行流量（GB)'] = sz_2['上行流量（GB)'].astype(np.float64)
# sz_2['下行流量（GB)'] = sz_2['下行流量（GB)'].astype(np.float64)
# sz_2['上行利用率(%)'] = sz_2['上行利用率(%)'].astype(np.float64)
# sz_2['下行利用率(%)'] = sz_2['下行利用率(%)'].astype(np.float64)
# sz_2['CCE利用率(%)'] = sz_2['CCE利用率(%)'].astype(np.float64)
# sz_2['RRC有效平均连接用户数（个）'] = sz_2['RRC有效平均连接用户数（个）'].astype(np.float64)
# sz_2['用户面平均上行速率(Mbps)'] = sz_2['用户面平均上行速率(Mbps)'].astype(np.float64)
# sz_2['用户面平均下行速率(Mbps)'] = sz_2['用户面平均下行速率(Mbps)'].astype(np.float64)
# sz_2['用户面平均上行时延(ms)'] = sz_2['用户面平均上行时延(ms)'].astype(np.float64)
# sz_2['E-RAB流量(KB)'] = sz_2['E-RAB流量(KB)'].astype(np.float64)
# sz_2['小区RB上行平均干扰电平(dBm)'] = sz_2['小区RB上行平均干扰电平(dBm)'].astype(np.float64)
# print(sz_2.info())
# sz_2 .to_csv('D:\shenzhen\Result\D.csv',header=1,encoding='gbk',index=False) #保存列名存储
# shenzhen_CGI = pd.read_csv('D:\shenzhen\szcgi.csv',encoding='gbk')
# sz = sz_1.append(sz_2)
# sz = sz.drop_duplicates()
# # sz = sz.loc[(~sz['CGI'].isin(shenzhen_CGI['CGI']))]
# print(sz.iloc[:,0].size)
# print(sz.columns)


def f(x):

    if x.max() > 0.5:
        return '是'
    if  np.isnan(x.max()):
        return ''
    else:
        return '否'

rl = pd.read_csv('D:\guangdong\zhoumangshi1027-1102.csv',encoding='gbk')
rl = rl.drop_duplicates('小区ID')
print(rl.columns)
gfhpg = rl[['小区ID','平均E-RAB数','有效RRC连接平均数','上行PRB平均利用率(v2.8)','上行业务信道流量(MB)','下行PRB平均利用率(v2.8)',
            '下行业务信道流量(MB)','PDCCH信道CCE占用率']]
gfhjg = pd.read_csv('D:\gxt\gfhjg.csv',encoding='gbk')
# BH_AVG_ERAB = pd.read_csv('D:\gxt\BH_AVG_ERAB.csv',encoding='gbk')
# gfhpg = pd.read_csv('D:\gxt\gfhpg.csv',encoding='gbk')
gfhjg = gfhjg.drop_duplicates()
# print(gfhjg.columns)
# print(BH_AVG_ERAB.columns)
# BH_AVG_ERAB.columns = ['ECGI','自忙时平均E-RAB流量（MB）']
# # print(gfhpg.columns)
# gfhpg = gfhpg[['小区ID','有效RRC连接平均数','上行PRB平均利用率(v2.8)','上行业务信道流量(MB)','下行PRB平均利用率(v2.8)',
#                '下行业务信道流量(MB)','PDCCH信道CCE占用率']]
gfhpg.columns =['ECGI', '自忙时平均E-RAB流量（MB）','有效RRC连接平均数：', '上行PRB平均利用率(%)：','上行吞吐量（MB）：', '下行PRB平均利用率(%)：',
                '下行吞吐量（MB）：', 'PDCCH信道CCE占用率(%)：']
print(gfhpg.columns)
gfhjg = gfhjg[['ECGI']]
print(gfhjg.iloc[:,0].size)
# gfhjg = pd.merge(gfhjg,BH_AVG_ERAB, on=['ECGI'], how='left',suffixes=('', '_y'))  # pandas csv表左连接
gfhjg = pd.merge(gfhjg,gfhpg, on=['ECGI'], how='left',suffixes=('', '_y'))  # pandas csv表左连接
gfhjg = gfhjg.drop_duplicates('ECGI')
gfhjg['是否高流量预警'] = gfhjg[['上行PRB平均利用率(%)：', '下行PRB平均利用率(%)：', 'PDCCH信道CCE占用率(%)：']].apply(f, axis=1)
gfhjg['有效RRC连接平均数：'] = gfhjg['有效RRC连接平均数：'].astype(np.float64)
gfhjg['包分类'] = np.where(gfhjg['自忙时平均E-RAB流量（MB）'] >= 1000, '大包',
                        np.where(((gfhjg['自忙时平均E-RAB流量（MB）'] >= 300) & (gfhjg['自忙时平均E-RAB流量（MB）'] < 1000)), '中包',
                                 np.where(gfhjg['自忙时平均E-RAB流量（MB）'].isnull(),'','小包')))
gfhjg['是否高负荷待扩容'] = np.where((((gfhjg['包分类']=='大包' )&(gfhjg['有效RRC连接平均数：']>10))&(((gfhjg['上行PRB平均利用率(%)：']>0.5)&(gfhjg['上行吞吐量（MB）：']>307.2))|(((gfhjg['下行PRB平均利用率(%)：']>0.7)|(gfhjg['PDCCH信道CCE占用率(%)：']>0.5))&(gfhjg['下行吞吐量（MB）：']>5120)))),'是',
                             np.where((((gfhjg['包分类']=='中包')&(gfhjg['有效RRC连接平均数：']>20))&(((gfhjg['上行PRB平均利用率(%)：']>0.5)&(gfhjg['上行吞吐量（MB）：']>307.2))|(((gfhjg['下行PRB平均利用率(%)：']>0.5)|(gfhjg['PDCCH信道CCE占用率(%)：']>0.5))&(gfhjg['下行吞吐量（MB）：']>3584)))),'是',
                                      np.where((((gfhjg['包分类']=='小包')&(gfhjg['有效RRC连接平均数：']>50))&(((gfhjg['上行PRB平均利用率(%)：']>0.5)&(gfhjg['上行吞吐量（MB）：']>307.2))|(((gfhjg['下行PRB平均利用率(%)：']>0.4)|(gfhjg['PDCCH信道CCE占用率(%)：']>0.5))&(gfhjg['下行吞吐量（MB）：']>2252.8)))),'是',
                                               np.where(((gfhjg['包分类']=='')|(gfhjg['是否高流量预警']=='')),'','否'))))
gfhjg.drop(['包分类'], axis=1,inplace=True)
print(gfhjg.info())
print(gfhjg.iloc[:,0].size)
#gfhjg.to_csv('D:\gxt\gfhjg1.csv',header=1,encoding='gbk',index=False)