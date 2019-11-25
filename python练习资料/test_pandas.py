import numpy as np
import pandas as pd
import re
import json

# 你可以使用value_counts（）方法查看有多少种分类存在
df = pd.DataFrame({"id":[1001,1002,1003,1004,1005,1006],
 "date":pd.date_range('20130102', periods=6),
  "city":['Beijing ', 'shanghai', ' guangzhou ', 'Shenzhen', 'shanghai', 'BEIJING '],
 "age":[23,44,54,32,34,32],
 "category":['100-A','100-B','110-A','110-C','210-A','130-F'],
  "price":[4200,np.nan,2133,5433,np.nan,4432]}
 )
df['city']= df['city'].str.capitalize()#转换大写
print(df)
print(df.shape) #纬度查看
print(df.info()) #数据表基本信息（维度、列名称、数据格式、所占空间等）
print(df['city'].dtypes)#某一列格式：
print(df.isnull())#空值：
print(df['city'].unique())#查看某一列的唯一值：

df.fillna(value=0,inplace=True)#用数字0填充空值
df['price'].astype('int') #更改数据格式
df['price'].fillna(df['price'].mean(),inplace=True)
df.rename(columns={'category': 'category-size'})
df['city'].drop_duplicates()
df['city'].drop_duplicates(keep='last')
df['city']=df['city'].str.capitalize()#转换大写
# df['city']=df['city'].str.upper()# 全部大写
df['city']=df['city'].map(str.strip) #清空空格
df['city']=df['city'].str.lower()#大小写转换
df['city'].replace('sh', 'shanghai',inplace=True)
# print(df.columns)

df1=pd.DataFrame({"id":[1001,1002,1003,1004,1005,1006,1007,1008],
"gender":['male','female','male','female','male','female','male','female'],
"pay":['Y','N','Y','Y','N','Y','N','Y',],
"m-point":[10,12,20,40,40,40,30,20]})
df_inner = pd.merge(df,df1,how='inner')  # 匹配合并，交集
df_left = pd.merge(df,df1,how='left')
df_right = pd.merge(df,df1,how='right')
df_outer = pd.merge(df,df1,how='outer')  #并集
df_inner['group'] = np.where(df_inner['price'] > 3000,'high','low')
# print(df_inner['group'])
zz = df_inner.loc[(df_inner['city'] == 'beijing') & (df_inner['price'] >= 4000), 'sign']=1
# print(zz)
# 对category字段的值依次进行分列，并创建数据表，索引值为df_inner的索引列，列名称为category和size
split = pd.DataFrame((x.split('-') for x in df_inner['category']),index=df_inner.index,columns=['category','size'])

print(split)
df_inner = pd.merge(df_inner,split,right_index=True, left_index=True,suffixes=('', '_y'))
# print(df_inner)
# print(df_inner.columns)
df_inner.set_index('id')
print(df_inner.index)
print(df_inner.sort_values(by=['age']))
# print(df_inner.sort_index())
# 判断city列里是否包含beijing和shanghai，然后将符合条件的数据提取出来
print(df_inner.loc[df_inner['city'].isin(['beijing','shanghai'])])
#使用与、或、非三个条件配合大于、小于、等于对数据进行筛选，并进行计数和求和。用“与”进行筛选
print(df_inner.loc[(df_inner['age'] > 25) & (df_inner['city'] == 'beijing'), ['id','city','age','category','gender']])

df_inner.loc[(df_inner['age'] > 25) | (df_inner['city'] == 'beijing'), ['id','city','age','category','gender']].sort_values(['age'])
a = df_inner.loc[(df_inner['city'] != 'beijing'), ['id','city','age','category','gender']].sort_values(['id'])
print(type(a))
print(a.head())

# print(df_inner.loc[(df_inner['city'] != 'beijing'), ['id','city','age','category','gender']].sort_values(by="id",ascending=False))
# 对筛选后的数据按city列进行计数
print(df_inner.loc[(df_inner['city'] != 'beijing'), ['id','city','age','category','gender']].sort_values(['id']).city.count())
# 使用query函数进行筛选
df_inner.query('city == ["beijing", "shanghai"]')
# 对筛选后的结果按prince进行求和
print(df_inner.query('city == ["beijing", "shanghai"]').price.sum())
# 数据汇总主要函数是groupby和pivote_table
# 对所有的列进行计数汇总
print(df_inner.groupby('city').count())
# 按城市对id字段进行计数
# print(df_inner.groupby('city')['id'].count())
# 对两个字段进行汇总计数
df_inner.groupby(['city','size'])['id'].count()
# 对city字段进行汇总，并分别计算prince的合计和均值
print(df_inner.groupby('city')['price'].agg([len,np.sum, np.mean]))
# 简单的数据采样
# print(df_inner.sample(n=3))
# 手动设置采样权重
weights = [0, 0, 0, 0, 0.5, 0.5]
# print(df_inner.sample(n=2, weights=weights))
# df2 =df1.drop(df['id'].isin(df['id']))
# print(df2)
data = pd.DataFrame({'id':[1,1,1,2,2,2],'value':['A','B','C','D','E','F']})
# data['value'] = data['value'].apply(lambda x:','+ x)
# data1 = data.groupby(by='id').sum()
# print(data1)
# data1['value'] = data1['value'].apply(lambda x :[x[1:]])
# print(data1)
##################################
data1 = data.groupby(by='id').apply(lambda x: [','.join(x['value'])])
print(data1)
############################################
def func(x):
    return x.isalnum()
seq = ["foo", "x41", "?!", "***"]
print(list(filter(func, seq)))
###############################################
m = re.match(r'www\.(.*)\..', 'www.python.org')
print(m.group(1))
print(m.group(0))
print(m.start(1))
print(m.end(1))
print(m.span(1))
####################################################
# emphasis_pattern = re.compile(r'''
# ... \* # 起始突出标志——一个星号
# ... ( # 与要突出的内容匹配的编组的起始位置
# ... [^\*]+ # 与除星号外的其他字符都匹配
# ... ) # 编组到此结束
# ... \* # 结束突出标志
# ... ''', re.VERBOSE)
####################################################
# emphasis_pattern = r'\*([^\*]+)\*'
# print(re.sub(emphasis_pattern, r'<em>\1</em>', 'Hello, *world*!'))
#######贪婪模式匹配
# emphasis_pattern = r'\*(.+)\*'
# emphasis_pattern = r'^*'
emphasis_pattern = r'\*\*(.+?)\*\*'
print(re.sub(emphasis_pattern, r'<em>\1</em>', '*This* is *it*!'))
print(re.sub(emphasis_pattern, r'<em>\1</em>', '**This** is **it**!'))

# print(df[['age','price']].cov())