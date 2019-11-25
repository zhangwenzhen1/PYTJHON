import openpyxl
import xlrd
import pandas as pd
from pandas import DataFrame
import numpy as np

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
    alldata = alldata.append(e)

print(len(alldata))
alldata['support_FDD用户数占比'] = alldata['support_FDD用户数']/alldata['用户数']
alldata= alldata.reset_index(drop=True)
#保存为新的sheet,首先新建sheet,合并后的数据保存到新sheet中
writer=pd.ExcelWriter(r'D:\guangdong\FDD_Count1.xlsx')
alldata.to_excel(writer,sheet_name="total",index=False)
writer.save()