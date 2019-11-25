import pandas as pd
import os
import numpy as np

path = r'D:\GD'  #指定存放文件的地址
file_name_list = os.listdir(path)   #返回.xlsx格式所有文件名的列表list
#for循环获取所有.xlsx格式文件的绝对地址的列表list
file_dir_list=[os.path.join(path,x) for x in file_name_list]
print(file_dir_list)
print(len(file_dir_list))
#定义DataFrame类型的变量df用来存放获取的所有数据
df = pd.DataFrame()
j=0
#for循环逐个读取每个Excel里面的数据
for i in file_name_list:
    if j in range(0,len(file_dir_list)):
        if (i[-4:] == 'xlsx'):  # 筛选只读取xlsx结尾的文件
            # read_excel方法，参数sheet_name表示读取的工作簿，skiprows表示忽略几行，usecols表示读取指定的列
            EXCEL1 = pd.read_excel(file_dir_list[j])
            # concat方法合并多个文件的数据
            df = pd.concat([df, EXCEL1], ignore_index=True)
            j=j+1
print(df.iloc[:,0].size)
# df.to_csv('D:\GD\oas1.csv',header=1,encoding='gbk',index=False) #保存列名存储

df['聚类问题点生成时间'] = pd.to_datetime(df['聚类问题点生成时间'],format='%Y/%m/%d %H:%M:%S')
df['详细问题点发生时间'] = pd.to_datetime(df['详细问题点发生时间'],format='%Y/%m/%d %H:%M:%S')
df = df.sort_values(by=['cgi','详细问题点类型','聚类问题点生成时间','详细问题点发生时间'],ascending=[True,True,False,False])
print(df.iloc[:,0].size)
# df.to_csv('D:\GD\oas1.csv',header=1,encoding='gbk',index=False) #保存列名存储
df = df.drop_duplicates(['cgi','详细问题点类型'],keep='first')
print(df.iloc[:,0].size)

df_1 = df.groupby(['地市归属'])['cgi'].count()
df_2 = df.loc[(df['评估结果'] == '通过')]
df_2 = df_2.groupby(['地市归属'])['cgi'].count()

df_1 = df_1.to_frame()
df_2 = df_2.to_frame()
df_result = pd.merge(df_1,df_2,on = '地市归属',how='outer',suffixes=('', '_y'))
df_result.columns = ['派单数','评估通过数']
df_result.fillna(0,inplace = True)
df_result.loc['全省'] = df_result.apply(lambda y: y.sum())
df_result['解决率'] = df_result['评估通过数']*1.0/df_result['派单数']
df_result = df_result.reindex(['全省','广州','深圳','东莞','佛山','汕头','珠海','惠州','中山','江门','湛江','茂名','揭阳','韶关','河源','梅州','汕尾','阳江','肇庆','清远','潮州','云浮'])
writer_1 = pd.ExcelWriter('D:\GDresult\gdcountresult.xlsx')
df.to_excel(writer_1,'volte最新工单表',index=False,encoding='gbk')
df_result.to_excel(writer_1,'volte工单统计结果',index=True,encoding='gbk')
# df_2.to_excel(writer_1,'投诉问题分类表',index=True,encoding='gbk')
# df_3.to_excel(writer_1,'域表',index=True,encoding='gbk')

writer_1.save()