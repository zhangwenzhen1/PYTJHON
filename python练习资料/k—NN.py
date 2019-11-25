import mglearn
import matplotlib.pylab as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from sklearn.datasets import make_blobs
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.datasets import load_boston
# from scikit_learn import make_blobs_directly

#生成forge数据集
X,y = mglearn.datasets.make_forge()
#绘制散点图
mglearn.discrete_scatter(X[:,0],X[:,1],y)
plt.legend(["Classic 0","Classic 1"],loc =4)
plt.xlabel("First feature")
plt.ylabel("Second feature")
print("X.shape:{}".format(X.shape))
plt.show()

#生成wave数据集
X,y = mglearn.datasets.make_wave(n_samples=40)
plt.plot(X,y,'o')
plt.ylim(-3,3)
plt.xlabel("Feature")
plt.ylabel("Target")
plt.show()

cancer =load_breast_cancer()
print("cancer.keys(): \n{}".format(cancer.keys()))
print("Shape of cancer data:{}".format(cancer.data.shape))
print("Sample counts per class :\n{}".format(
    {n: v for n, v in zip(cancer.target_names,np.bincount(cancer.target))}))
print(" Feature names:\n{}".format(cancer.feature_names))


boston = load_boston()
print("Data shape:{}".format(boston.data.shape))

X,y = mglearn.datasets.load_extended_boston()
print("X.shape:{}".format(X.shape))

mglearn.plots.plot_knn_classification(n_neighbors=1)
plt.show()

mglearn.plots.plot_knn_classification(n_neighbors=3)
plt.show()

#####################################################################################################

from sklearn.neighbors import KNeighborsClassifier
#生成forge数据集

X,y = mglearn.datasets.make_forge()
###导入数据，实例化，并设置参数 random_state:参数指定随机生成数的种子，这样函数输出就是固定不变的。
X_train,X_test,y_train,y_test =train_test_split(X,y,random_state=0)

clf = KNeighborsClassifier(n_neighbors=3)

#######调用fit方法构建模型，传入训练数据X_train，输出数据y_train
clf.fit(X_train,y_train)

###调用predict 方法对测试数据集预测
print("Test set predictions:{}".format(clf.predict(X_test)))

####调用score方法，评估模型的泛华能力好坏
print("Test set accuracy: {:.2f}".format(clf.score(X_test,y_test)))

fig, axes = plt.subplots(1,3,figsize=(10,3))

for n_neighbors,ax in zip([1,3,9],axes):
    #fit方法返回对象本身，所以可以将实例化和拟合放在一行代码中
    clf = KNeighborsClassifier(n_neighbors = n_neighbors).fit(X,y)
    mglearn.plots.plot_2d_separator(clf,X,fill=True,eps=0.5,ax=ax,alpha=0.4)
    mglearn.discrete_scatter(X[:,0],X[:,1],y,ax=ax)
    ax.set_title("{} neighbor(s)".format(n_neighbors))
    ax.set_xlabel("feature 0")
    ax.set_ylabel("feature 1")
axes[0].legend(loc=3)

plt.show()


###################################
cancer = load_breast_cancer()
###导入数据，实例化，并设置参数
X_train,X_test,y_train,y_test =train_test_split(cancer.data,cancer.target,stratify= cancer.target,random_state=66)

training_accuracy =[]
test_accuracy =[]
#n_neighbors取值从1到10
neighbors_settings =range(1,11)
for n_neighbors in neighbors_settings:
    #构建模型
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    clf.fit(X_train,y_train)
    #记录训练精度
    training_accuracy.append(clf.score(X_train,y_train))
    #记录泛化精度
    test_accuracy.append(clf.score(X_test,y_test))
plt.plot(neighbors_settings,training_accuracy,label='training accuracy')
plt.plot(neighbors_settings,test_accuracy,label='test accuracy')
plt.ylabel('Accuracy')
plt.xlabel('n_neighbors')
plt.legend()
plt.show()

#k近邻回归
mglearn.plots.plot_knn_regression(n_neighbors=1)
plt.show()

mglearn.plots.plot_knn_regression(n_neighbors=3)
plt.show()

from sklearn.neighbors import KNeighborsRegressor

X,y = mglearn.datasets.make_wave(n_samples=40)

X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=0)

#模型实例化
reg = KNeighborsRegressor(n_neighbors =3)

#利用训练数据和训练目标值来拟合模型
reg.fit(X_train,y_train)

print("Test set predictions: \n{}".format(reg.predict(X_test)))

print("Test set R^2; {:.2f}".format(reg.score(X_test,y_test)))

fig,axes = plt.subplots(1,3,figsize=(15,4))
#创建1000个数据点，在-3,3之间均匀分布
line = np.linspace(-3,3,1000).reshape(-1,1)
for n_neighbors,ax in zip([1,3,9],axes):
    #利用1,3,9个邻居分别预测
    reg = KNeighborsRegressor(n_neighbors=n_neighbors)
    reg.fit(X_train,y_train)
    xmajorLocator = MultipleLocator(1)  # 将x主刻度标签设置为1的倍数
    xmajorFormatter = FormatStrFormatter('%5.1f')  # 设置x轴标签文本的格式
    xminorLocator = MultipleLocator(0.5)  # 将x轴次刻度标签设置为5的倍数

    ymajorLocator = MultipleLocator(0.5)  # 将y轴主刻度标签设置为0.5的倍数
    ymajorFormatter = FormatStrFormatter('%1.1f')  # 设置y轴标签文本的格式
    yminorLocator = MultipleLocator(0.1)  # 将此y轴次刻度标签设置为0.1的倍数

    # 显示次刻度标签的位置,没有标签文本
    ax.xaxis.set_minor_locator(xminorLocator)

    ax.plot(line,reg.predict(line))
    ax.plot(X_train,y_train,'^',c=mglearn.cm2(0),markersize=8)
    ax.plot(X_test, y_test, 'o', c=mglearn.cm2(1), markersize=8)
    ax.set_title(
        "{} neighbor(s)\n train score:{:.2f} test score: {:.2f}".format(
            n_neighbors,reg.score(X_train,y_train),
            reg.score(X_test,y_test))
    )
    ax.set_xlabel("Feature")
    ax.set_ylabel("Target")

    # 设置主刻度标签的位置,标签文本的格式
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.xaxis.set_major_formatter(xmajorFormatter)

    ax.yaxis.set_major_locator(ymajorLocator)
    ax.yaxis.set_major_formatter(ymajorFormatter)

    # 显示次刻度标签的位置,没有标签文本
    ax.xaxis.set_minor_locator(xminorLocator)
    ax.yaxis.set_minor_locator(yminorLocator)

    ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
    ax.yaxis.grid(True, which='minor')  # y坐标轴的网格使用次刻度

    axes[0].legend(["Model predictions","Train data/target",
                   "Test data/target"],loc="best")

plt.show()