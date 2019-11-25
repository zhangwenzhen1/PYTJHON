import pandas as pd
import numpy as np
df = pd.read_csv('D:\cqtfqd0918.csv',encoding='gbk',error_bad_lines=False)
df['片区'] = np.where(df['所属地市'].isin(['广州','珠海','江门','中山','肇庆','云浮']),'粤中组',
                    np.where(df['所属地市'].isin(['深圳','惠州','揭阳','汕头','汕尾']),'粤东南',
                             np.where(df['所属地市'].isin(['佛山','湛江','茂名','清远','韶关','阳江']),'粤西北','粤东北')))

df_1 = df.groupby('所属地市')['CGI'].agg([len])
df_1.loc['全省'] = df_1.apply(lambda x: x.sum())
df_1 = df_1.reset_index(drop=False)
df_1.columns = ['所属地市','退服数']
df_2 = df.groupby('片区')['CGI'].agg(len)
df_2 = df_2.reset_index(drop=False)
df_2.columns = ['所属地市','退服数']
df_3 = df_1.append(df_2)
df_3.set_index('所属地市',inplace=True)
df_3 = df_3.reindex(['广州','珠海','江门','中山','肇庆','云浮','粤中组','深圳','惠州','揭阳','汕头','汕尾','粤东南',
                     '佛山','湛江','茂名','清远','韶关','阳江','粤西北','东莞','梅州','河源','潮州','粤东北','全省'])
df_3.to_csv('D:\guangdong\测试.csv',header=1,encoding='gbk') #保存列名存储
