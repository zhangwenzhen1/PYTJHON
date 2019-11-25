# os：本地文件夹创建
# urllib：web路径的解析，数据文件下载
# tarfile：压缩文件的解压
# 获取数据
import os
import tarfile
from six.moves import urllib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
# ##################################################################################
# DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
# HOUSING_PATH = "datasets/housing"
# HOUSING_URL = DOWNLOAD_ROOT + HOUSING_PATH + "/housing.tgz"
#
# def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
#     """
#     获取数据
#     输入文件链接
#     """
#     if not os.path.isdir(housing_path):
#         os.makedirs(housing_path)               # 如果没有目标文件夹则创建一个
#     tgz_path = os.path.join(housing_path, "housing.tgz")
#                                                 # 路径组合
#     urllib.request.urlretrieve(housing_url, tgz_path)
#                                                 # 将rul数据保存在path
#     housing_tgz = tarfile.open(tgz_path)        # 解压
#     housing_tgz.extractall(path=housing_path)   # 提取文本内容
#     housing_tgz.close()
#
# def load_housing_data(housing_path=HOUSING_PATH):
#     """
#     加载数据
#     输入参数：
#     文件路径
#     """
#     csv_path = os.path.join(housing_path, "housing.csv")
#     return pd.read_csv(csv_path)
#
# # [].value_counts()：类别型特征的计数统计
# fetch_housing_data()
# housing = load_housing_data()
#
# #######################################################################

housing= pd.read_csv('D:\guangdong\housing.csv',encoding='gbk')
print(housing.head())                         # 查看数据前五行
print(housing.info())                         # 查看数据基本信息
print(housing["ocean_proximity"].value_counts())# 对类别数据计数统计
print(housing.describe())                     # 查看数值型数据的基本统计信息
# # 绘制数值型数据的直方图

housing.hist(bins=50, figsize=(20, 15))       # bins指定箱子个数
                                              # figsize子图大小
plt.show()

# 方法一：调用Scikit-Learn库进行数据分割
train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)

#方法二：数据分割，数据按比例分
#自写函数通过随机直接分割数据
def split_train_test(data, test_ratio):
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]

# 这两种解决方案在下一次获取更新的数据时都会中断。常见的解决办法是每个实例都使用一个标识符（identifier）来决定是否
# 进入测试集（假定每个实例都有一个唯一且不变的标识符）。举例来说，你可以计算每个实例标识符的hash值，只取hash的最后一个字
# 节，如果该值小于等于51（约256的20%），则将该实例放入测试集。这样可以确保测试集在多个运行里都是一致的，即便更新数据集
# 也仍然一致。新实例的20%将被放入新的测试集，而之前训练集中的实例也不会被放入新测试集

import hashlib
def test_set_check(identifier, test_ratio, hash):
    return hash(np.int64(identifier)).digest()[-1] < 256 * test_ratio

# 不幸的是，housing数据集没有标识符列。最简单的解决方法是使用行索引作为ID：
#方法三：数据分割，
#自写函数通过哈希编码+随机分割数据
def split_train_test_by_id(data, test_ratio, id_column, hash=hashlib.md5):
    ids = data[id_column]
    in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio, hash))
    return data.loc[~in_test_set], data.loc[in_test_set]

housing_with_id = housing.reset_index() # adds an `index` column
train_set, test_set = split_train_test_by_id(housing_with_id, 0.2, "index")
train_set.to_csv('D:\guangdong\Train_set.csv', header=1, encoding='gbk')
test_set.to_csv('D:\guangdong\Test_set.csv', header=1, encoding='gbk')
# 分层抽样
# 创建收入类别属性的：将收入中位数除以1.5（限制收入类别的数量），然后使用ceil进行取整（得到离散类别），最后
# 将所有大于5的类别合并为类别5
housing["income_cat"] = np.ceil(housing["median_income"] / 1.5)
housing["income_cat"].where(housing["income_cat"] < 5, 5.0, inplace=True)
# housing.to_csv('D:\guangdong\housing1.csv',header=1,encoding='gbk')

from sklearn.model_selection import StratifiedShuffleSplit #分层抽样

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

for train_index, test_index in split.split(housing, housing["income_cat"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]

print(housing["income_cat"].value_counts() / len(housing))

#删除income_cat属性，将数据恢复原样
for set in (strat_train_set, strat_test_set):
    set.drop(["income_cat"], axis=1, inplace=True)

housing = strat_train_set.copy()

housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.1)
                                              # alpha 设置散点的透明度
plt.show()
# 基于房屋价格的**图
# 每个圆的半径大小代表了每个地区的人口数量（选项s），颜色代表价格（选项c）。我们使用一
# 个名叫jet的预定义颜色表（选项cmap）来进行可视化，颜色范围从蓝（低）到红（高）
housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.4,
  s=housing["population"]/100, label="population",
  # 采用人口数量为半径画圆，增加图例说明
  c="median_house_value", cmap=plt.get_cmap("jet"), colorbar=True,
  # 人口数量的圆圈用房屋中位数价格填充，颜色选取默尔的颜色映射
)
plt.legend()
plt.show()
corr_matrix = housing.corr()
print(corr_matrix)
print(corr_matrix["median_house_value"].sort_values(ascending=False))

# 绘制出每个数值属性相对于其他数值属性的相关性。
from pandas.tools.plotting import scatter_matrix

attributes = ["median_house_value", "median_income", "total_rooms",
"housing_median_age"]
scatter_matrix(housing[attributes], figsize=(12, 8))
plt.show()

housing.plot(kind="scatter", x="median_income", y="median_house_value",
alpha=0.1)

plt.show()

housing["rooms_per_household"] = housing["total_rooms"]/housing["households"]
housing["bedrooms_per_room"] = housing["total_bedrooms"]/housing["total_rooms"]
housing["population_per_household"]=housing["population"]/housing["households"]
corr_matrix = housing.corr()
print(corr_matrix["median_house_value"].sort_values(ascending=False))

# 先回到一个干净的数据集（再次复制strat_train_set），然后将预测器和标签分开，
# 因为这里我们不一定对它们使用相同的转换方式（需要注意drop（）会创建一个数据副本，
# 但是不影响strat_train_set）
# Machine Learning数据准备
housing = strat_train_set.drop("median_house_value", axis=1)
housing_labels = strat_train_set["median_house_value"].copy()

# ·放弃这些相应的地区
# ·放弃这个属性
# ·将缺失的值设置为某个值（0、平均数或者中位数等都可以）
###########################################################
# housing.dropna(subset=["total_bedrooms"]) # option 1
# housing.drop("total_bedrooms", axis=1) # option 2
# median = housing["total_bedrooms"].median()
# housing["total_bedrooms"].fillna(median) # option 3
###########################################################

# Imputer用于填充缺失值
# Pipeline用于组合各种数据处理方法
# FeatureUnion用于联合多个Pipeline
from sklearn.preprocessing import Imputer
imputer = Imputer(strategy="median")
# 由于中位数值只能在数值属性上计算，所以我们需要创建一个没
# 有文本属性的数据副本ocean_proximity：
housing_num = housing.drop("ocean_proximity", axis=1)
# 使用fit（）方法将imputer实例适配到训练集
imputer.fit(housing_num)
print(imputer.statistics_)
print(housing_num.median().values)

X = imputer.transform(housing_num) #结果是一个包含转换后特征的Numpy数组

# 将它放回Pandas DataFrame
housing_tr = pd.DataFrame(X, columns=housing_num.columns)

# 之前排除了分类属性ocean_proximity，它是一个文本属性，无法计算它的中位数值。大部分的机器学习算法都更易于跟
# 数字打交道，先将这些文本标签转化为数字

     #从文本类别转化为整数类别
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
housing_cat = housing["ocean_proximity"]
housing_cat_encoded = encoder.fit_transform(housing_cat)
print("housing_cat_encoded:{}".format(housing_cat_encoded))
# print(housing_cat_encoded)
print(len(housing_cat_encoded))
print(encoder.classes_)
    #从整数类别转换为独热向量
from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder()
housing_cat_1hot = encoder.fit_transform(housing_cat_encoded.reshape(-1,1))
print(housing_cat_1hot)
print(housing_cat_1hot.toarray())

# 用LabelBinarizer类可以一次性完成两个转换（从文本类别转化为整数类别，再从整数类别转换为独热向量）
# 注:这时默认返回的是一个密集的NumPy数组。通过发送
# sparse_output=True给LabelBinarizer构造函数，可以得到稀疏矩阵。
from sklearn.preprocessing import LabelBinarizer
encoder = LabelBinarizer()
housing_cat_1hot = encoder.fit_transform(housing_cat)
print(housing_cat_1hot)

# 数据清理
from sklearn.base import BaseEstimator, TransformerMixin
rooms_ix, bedrooms_ix, population_ix, households_ix = 3, 4, 5, 6

class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    """
    属性融合
    """
    def __init__(self, add_bedrooms_per_room = True): # no *args or **kargs
        self.add_bedrooms_per_room = add_bedrooms_per_room
    def fit(self, X, y=None):
        return self  # nothing else to do
    def transform(self, X, y=None):
        rooms_per_household = X[:, rooms_ix] / X[:, households_ix]
        population_per_household = X[:, population_ix] / X[:, households_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            return np.c_[X, rooms_per_household, population_per_household,
                     bedrooms_per_room]
        else:
            return np.c_[X, rooms_per_household, population_per_household]

attr_adder = CombinedAttributesAdder(add_bedrooms_per_room=False)
print(attr_adder)
print(type(housing))
housing_extra_attribs = attr_adder.transform(housing.values)
print(housing_extra_attribs)

##########################################################################

class DataFrameSelector(BaseEstimator, TransformerMixin):
    """Scikit-Learn不能直接处理Pandas的DataFrame"""
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.attribute_names].values
#
from sklearn.preprocessing import LabelBinarizer
class MylabelBinarizer(TransformerMixin):
    """Scikit-Learn 0.19与0.18种的 LabelBinarizer 不同"""
    def __init__(self, *args, **kwargs):
        self.encoder = LabelBinarizer(*args, **kwargs)
    def fit(self, x, y=0):
        self.encoder.fit(x)
        return self
    def transform(self, x, y=0):
        return self.encoder.transform(x)

###########################################################################
                            ######数据缩放#######
#### 最小-最大缩放（又叫作归一化）很简单：将值重新缩放使其最终范围归于0到1之间。实现方法是将值减去最小值并除以最大值和最
# 小值的差。对此，Scikit-Learn提供了一个名为MinMaxScaler的转换器。如果出于某种原因，你希望范围不是0～1，你可以通过调整超参
# 数feature_range进行更改。
####标准化则完全不一样：首先减去平均值（所以标准化值的均值总是零），然后除以方差，从而使得结果的分布具备单位方差。不同于
# 最小-最大缩放的是，标准化不将值绑定到特定范围，对某些算法而言，这可能是个问题（例如，神经网络期望的输入值范围通常是0到
# 1）。但是标准化的方法受异常值的影响更小。例如，假设某个地区的平均收入等于100（错误数据）。最小-最大缩放会将所有其他值从
# 0～15降到0～0.15，而标准化则不会受到很大影响。Scikit-Learn提供了一个标准化的转换器StandadScaler。
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
num_pipeline = Pipeline([
('imputer', Imputer(strategy="median")),
('attribs_adder', CombinedAttributesAdder()),
('std_scaler', StandardScaler()),
])
print(housing_num.info())
housing_num_tr = num_pipeline.fit_transform(housing_num)

from sklearn.pipeline import FeatureUnion
# from sklearn_features.transformers import DataFrameSelector
num_attribs = list(housing_num)
cat_attribs = ["ocean_proximity"]

# num_pipeline = Pipeline([('selector',DataFrameSelector(num_attribs)),
#                          ('imputer', Imputer(strategy="median")),
#                          ('attribs_adder', CombinedAttributesAdder()),
#                          ('std_scaler', StandardScaler()),])
#
# cat_pipeline = Pipeline([('selector', DataFrameSelector(cat_attribs)),
#                          ('label_binarizer', LabelBinarizer()),])
#
# full_pipeline = FeatureUnion(transformer_list=[("num_pipeline", num_pipeline),
#                                                ("cat_pipeline", cat_pipeline),])
print(housing.info())
# housing_prepared = full_pipeline.fit_transform(housing)

#
num_pipeline = Pipeline([
    ('selector', DataFrameSelector(num_attribs)),
    ('imputer', Imputer(strategy="median")),
    ('attribs_adder', CombinedAttributesAdder()),
    ('std_scaler', StandardScaler()),
    ])
cat_pipeline = Pipeline([
    ('selector', DataFrameSelector(cat_attribs)),
    ('label_binarizer', MylabelBinarizer()),
    ])
full_pipeline = FeatureUnion(transformer_list=[
    ('num_pipeline', num_pipeline),
    ('cat_pipeline', cat_pipeline),
    ])
housing_prepared = full_pipeline.fit_transform(housing)
print(housing_prepared)
print(housing_prepared.shape)

from sklearn.linear_model import LinearRegression
lin_reg = LinearRegression()
lin_reg.fit(housing_prepared, housing_labels)

some_data = housing.iloc[:5]
some_labels = housing_labels.iloc[:5]
some_data_prepared = full_pipeline.transform(some_data)
print("Predictions:\t", lin_reg.predict(some_data_prepared))
print("Labels:\t\t", list(some_labels))

from sklearn.metrics import mean_squared_error
housing_predictions = lin_reg.predict(housing_prepared)
lin_mse = mean_squared_error(housing_labels, housing_predictions)
lin_rmse = np.sqrt(lin_mse)
print(lin_rmse)


# 决策树回归
from sklearn.tree import DecisionTreeRegressor
tree_reg = DecisionTreeRegressor()
tree_reg.fit(housing_prepared, housing_labels)
housing_predictions = tree_reg.predict(housing_prepared)
tree_mse = mean_squared_error(housing_labels, housing_predictions)
tree_rmse = np.sqrt(tree_mse)
print(tree_rmse)

# 0  过拟合
# 交叉验证
from sklearn.model_selection import cross_val_score
scores = cross_val_score(tree_reg, housing_prepared, housing_labels,
                         scoring="neg_mean_squared_error", cv=10)
# Scikit-Learn的交叉验证功能更倾向于使用效用函数（越大越好）而不是成本函数（越小越好），所以计算分数的函数实际上是负
# 的MSE（一个负值）函数，这就是为什么上面的代码在计算平方根之前会先计算出-scores。
tree_rmse_scores = np.sqrt(-scores)                              # 返回10次结果
# 结果显示
def display_scores(scores):
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation:", scores.std())
display_scores(tree_rmse_scores)

lin_scores = cross_val_score(lin_reg, housing_prepared, housing_labels,
                             scoring="neg_mean_squared_error", cv=10)

lin_rmse_scores = np.sqrt(-lin_scores)
display_scores(lin_rmse_scores)

# 随机森林
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
forest_reg = RandomForestRegressor()
forest_reg.fit(housing_prepared, housing_labels)
housing_predictions = forest_reg.predict(housing_prepared)
forest_mse = mean_squared_error(housing_labels, housing_predictions)
forest_rmse = np.sqrt(forest_mse)
print(forest_rmse) # 21925.
forest_scores = cross_val_score(forest_reg, housing_prepared, housing_labels,
                                scoring="neg_mean_squared_error", cv=10)
forest_rmse_scores = np.sqrt(-forest_scores)
display_scores(forest_rmse_scores)

# 每一个尝试过的模型你都应该妥善保存，这样将来你可以轻松回到你想要的模型当中。记得还要同时保存超参数和训练过的参
# 数，以及交叉验证的评分和实际预测的结果。这样你就可以轻松地对比不同模型类型的评分，以及不同模型造成的错误类型。通过Python
# 的pickel模块或是sklearn.externals.joblib，你可以轻松保存Scikit-Learn模型，这样可以更有效地将大型NumPy数组序列化：
'''
from sklearn.externals import joblib
joblib.dump(my_model, "my_model.pkl")
# and later...
my_model_loaded = joblib.load("my_model.pkl")
'''
# 调参 GridSearchCV
from sklearn.model_selection import GridSearchCV
param_grid = [
    {'n_estimators': [3, 10, 30], 'max_features': [2, 4, 6, 8]},
    {'bootstrap': [False], 'n_estimators': [3, 10], 'max_features': [2, 3, 4]}
    ]
forest_reg = RandomForestRegressor()
grid_search = GridSearchCV(forest_reg, param_grid, cv=5,
                           scoring='neg_mean_squared_error')
grid_search.fit(housing_prepared, housing_labels)
grid_search.best_params_
grid_search.best_estimator_
cvres = grid_search.cv_results_
for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
    print(np.sqrt(-mean_score), params)

feature_importances = grid_search.best_estimator_.feature_importances_
print(feature_importances)
extra_attribs = ["rooms_per_hhold", "pop_per_hhold", "bedrooms_per_room"]
cat_one_hot_attribs = list(encoder.classes_)
attributes = num_attribs + extra_attribs + cat_one_hot_attribs
print(sorted(zip(feature_importances, attributes), reverse=True))

# 通过测试集评估模型
final_model = grid_search.best_estimator_
X_test = strat_test_set.drop("median_house_value", axis=1)
y_test = strat_test_set["median_house_value"].copy()
X_test_prepared = full_pipeline.transform(X_test)
final_predictions = final_model.predict(X_test_prepared)
final_mse = mean_squared_error(y_test, final_predictions)
final_rmse = np.sqrt(final_mse) # => evaluates to 48,209.6
print(final_mse)