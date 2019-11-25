import pandas as pd
import numpy as np


# df = pd.read_csv('D:\Test\wzgxb.csv',encoding='gbk')
# df1 = pd.read_csv('D:\Test\hddsb.csv',encoding='gbk')
# df2 = pd.read_csv('D:\Test\City.csv',encoding='gbk')
# df = df.drop_duplicates('CGI')
# df['eNodebID'] = df['eNodebID'].astype(np.int64)
# df1['起号段'] = df1['起号段'].astype(np.int64)
# df1['止号段'] = df1['止号段'].astype(np.int64)
#
# print(df.iloc[:,0].size)
# i = 0
# while i< len(df1):
#    df['eNodebID_1'] = df1.iat[i,0]
#    df['city'] = df1.iat[i,2]
#    df['nub'] = df['eNodebID'] - df['eNodebID_1']
#    zb = df.loc[(df['nub'] <= 255) & (0 <= df['nub'])]
#    # df1 = df1.loc[(~df1['CGI'].isin(zb['CGI']))]
#    df2 = df2.append(zb)
#    i+=1
#
# df2 =df2[['ECI', '位置更新数', 'CGI', 'eNodebID','city']]
# df_2 = df.loc[(~df['CGI'].isin(df2['CGI']))]
# df_2 =df_2[['ECI', '位置更新数', 'CGI', 'eNodebID','city']]
# df_2['city'] = ''
# # df_2['nub'] = ''
# df2 = df2.append(df_2)
# print(df2.columns)
# print(df2.iloc[:,0].size)
# df2.to_csv('D:\Test\City1.csv',header=1,encoding='gbk',index=False) #保存列名存储