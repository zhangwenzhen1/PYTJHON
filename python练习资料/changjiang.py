import pandas as pd
import datetime
import numpy as np

# chagjing_1 = pd.read_csv('D:\gxt\zhongyaochangjing\changjing1.csv',encoding='gbk')
# chagjing_2 = pd.read_csv('D:\gxt\zhongyaochangjing\changjing2.csv',encoding='gbk')
# chagjing_1 =chagjing_1[['cgi','详细问题点类型','评估结果']]
# chagjing = pd.merge(chagjing_2,chagjing_1,on=['cgi','详细问题点类型'],how='left',suffixes=('', '_y')) # pandas csv表左连接
# chagjing.to_csv('D:\gxt\zhongyaochangjing\场景3.csv',header=1,encoding='gbk',index=False)
df = pd.read_csv('D:\gxt\zhongyaochangjing\R.csv',encoding='gbk')
# df = df.pivot(['地市归属','覆盖场景'],'评估结果','len')
df =pd.pivot_table(df,index=['地市归属','覆盖场景','评估结果'])
print(df.head())
df.to_csv('D:\gxt\zhongyaochangjing\df3.csv',header=1,encoding='gbk')