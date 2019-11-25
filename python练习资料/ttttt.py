# import pandas as pd
# import numpy as np

# gc = pd.read_csv('D:\guangdong\g1.csv',names=['地市','小区数','流量'],encoding='gbk')
# print(gc.head())
#
# df = pd.DataFrame([[1,2,3],[4,5,6]],columns=['a','b','c'])
# # df1 = pd.DataFrame([[7,8,9]],columns=['a','b','c'])
# # df.insert(0,'E',[11,12,13,14,15])     #插入一
# df.loc[2]=[7,8,9]
# # df =df.append(df1)
# print(df)
# #先将要添加进去的记录转置后连接在一起
# t = pd.concat([pd.DataFrame([7,8,9]).T,pd.DataFrame([10,11,12]).T])
# #然后修改columns 使得和df的columns一致
# t.columns = df.columns
# #最后把两个DataFrame合并并且忽略index
# df = pd.concat([df,t],ignore_index=True)
# print(df)
#
import openpyxl
import xlrd
import pandas as pd
from  pandas import DataFrame
import numpy as np
# ##读取workbook所有sheet
# wb = xlrd.open_workbook(r'D:\test1.xlsx')
# # 获取workbook中所有的表格
# sheets = wb.sheet_names()
# print(sheets)
#
# # 循环遍历所有sheet
# alldata = DataFrame()
# for i in range(len(sheets)):
#     df = pd.read_excel(r'D:\test1.xlsx', sheet_name=i, index=False, encoding='utf8')
#     df.columns =['e','f']###修改列名
#     print(df)
#     #df.loc[1]=[1,2]
#     alldata = alldata.append(df)
#
# #保存为新的sheet,首先新建sheet,合并后的数据保存到新sheet中
# writer=pd.ExcelWriter(r'D:\test2.xlsx')
# alldata.to_excel(writer,sheet_name="total",index=False)
# writer.save()

##读取workbook所有sheet
wb = xlrd.open_workbook(r'D:\guangdong\FDD_count.xlsx')
# 获取workbook中所有的表格
sheets = wb.sheet_names()
print(sheets)

# 循环遍历所有sheet
alldata = DataFrame()

for i in range(len(sheets)):
    df = pd.read_excel(r'D:\guangdong\FDD_count.xlsx', sheet_name=i, index=False, encoding='utf8')
    df['support_FDD'] = np.where((df['Band8（1为支持、0为不支持）']==1) |(df['Band3（1为支持、0为不支持）']==1),'是','否')
    ###用户数总数
    a = df['用户数'].sum()
    b = df.loc[(df['support_FDD']=='是')]
    ###support_FDD用户数总数
    c = b['用户数'].sum()
    d = sheets[i]
    e = [d,a,c]
    e = DataFrame(e).T
    e.columns =['地市','用户数','support_FDD用户数']
    print(e)
    alldata = alldata.append(e)
#alldata.reindex(range(22056))
print(len(alldata))
alldata['support_FDD用户数占比'] = alldata['support_FDD用户数']/alldata['用户数']
alldata= alldata.reset_index(drop=True)
#保存为新的sheet,首先新建sheet,合并后的数据保存到新sheet中
writer=pd.ExcelWriter(r'D:\guangdong\FDD_Count1.xlsx')
alldata.to_excel(writer,sheet_name="total",index=False)
writer.save()

