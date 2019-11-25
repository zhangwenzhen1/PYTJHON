import pandas as pd
import os
import numpy as np

df1 = pd.read_csv('D:\GD\V_volte_send20191028.csv',encoding='utf-8')
print(df1.iloc[:,0].size)
print(df1.info())
df2 = pd.read_csv('D:\GD\V_volte_returnvaluation20191028.csv',encoding='utf-8')
df2 =df2[['vcauxiliarypointer6', 'vcauxiliarypointer7', 'vcauxiliarypointer8','vcauxiliarypointer9',
          'vcauxiliarypointer12', 'vcauxiliarypointer13','vcauxiliarypointer14', 'vcauxiliarypointer15',
          'vcauxiliarypointer16','vcauxiliarypointer17', 'vcauxiliarypointer18', 'vcauxiliarypointer19',
          'vcauxiliarypointer20', 'vcauxiliarypointer21', 'vcauxiliarypointer24','vcauxiliarypointer28',
          'vcauxiliarypointer29', 'vcauxiliarypointer30']]
print(df2.iloc[:,0].size)
print(df2.columns)
df = pd.merge(df2,df1,on='vcauxiliarypointer6',how='outer',suffixes=('', '_y'))
df = df.loc[(df['vcauxiliarypointer24'].notnull())]
print(df.iloc[:,0].size)
df['vcauxiliarypointer24'] = pd.to_datetime(df['vcauxiliarypointer24'],format='%Y/%m/%d %H:%M:%S')
df['starttime'] = pd.to_datetime(df['starttime'],format='%Y/%m/%d %H:%M:%S')
df = df.sort_values(by=['vccgi','vcequestiontype','vcauxiliarypointer24','starttime'],ascending=[True,True,False,False])
df = df.drop_duplicates(['vccgi','vcequestiontype'],keep='first')
df.to_csv('D:\GDresult\gdresult_xiagdan1.csv',header=1,encoding='utf-8',)
df['vcauxiliarypointer19'] = np.where((((df['vcauxiliarypointer19'].isnull())|(df['vcauxiliarypointer19']=='未通过'))&
                                      (df['vcauxiliarypointer16']=='评估通过')),'通过',df['vcauxiliarypointer19'])
print(df.iloc[:,0].size)
# df.to_csv('D:\GDresult\gdresult_xiagdan.csv',header=1,encoding='utf-8',)
df['vcauxiliarypointer19'].fillna('未通过',inplace = True)
df_1 = df.pivot_table(df,index=['vcauxiliarypointer1'],columns=['vcauxiliarypointer19'],aggfunc={'vccgi':len},margins_name=True,)
df_1.columns = df_1.columns.droplevel()

df_1.fillna(0,inplace = True)
df_1.loc['全省'] = df_1.apply(lambda y: y.sum())

df = df.pivot_table(df,index=['vcauxiliarypointer1'],columns=['vcauxiliarypointer16'],aggfunc={'vccgi':len},margins_name=True,)
df.columns = df.columns.droplevel()

df.fillna(0,inplace = True)
df.loc['全省'] = df.apply(lambda y: y.sum())
df = df.reindex(['全省','广州','深圳','东莞','佛山','汕头','珠海','惠州','中山','江门','湛江','茂名','揭阳','韶关',
                  '河源','梅州','汕尾','阳江','肇庆','清远','潮州','云浮'])

print(df.head())
df = pd.merge(df,df_1,on='vcauxiliarypointer1',how='outer',suffixes=('', '_y'))
df['解决率'] = df['通过']*1.0/(df['通过']+df['未通过'])
# df.to_csv('D:\GDresult\gdresult_day.csv',header=1,encoding='gbk',)