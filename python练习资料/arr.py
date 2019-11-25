
import numpy as np
import pandas as pd

# arr = np.arange(32).reshape((8,4))
# print(arr)
# L1 = arr[:,:2]
# L2 = arr[:,2:]
# print(L1)
# # print(L2)
# # # L1[1:1] = L2
# # L1 = [[1, 2, 3, 4, 5],
# #       [7,8,9,10,11]]
# # L2 = [[20, 30, 40],[50,60,70]]
# # L1[5:5] = L2
# # print(L1.eval())

tem = pd.read_csv('D:\A.csv',encoding='utf-8')
b = tem.columns.str.lower()
b =list(b)
# print(b)
# print(type(b))
df = pd.read_csv('D:\Rnodb.M_PM_PRB_CELL_20190419.csv',encoding='utf-8',usecols=b,error_bad_lines=False,nrows=100)
# df.to_csv('D:\M_PM_PRB_CELL.csv',header=1,encoding='utf-8',index=False)
print(df.head())