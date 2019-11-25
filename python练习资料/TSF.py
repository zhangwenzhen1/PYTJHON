# import tensorflow as tf
# # # hello = tf.constant('hello, TensorFlow!')
# # sess = tf.Session()
# # print(sess.run(hello))
# # a = tf.add(2,4)
# # b = tf.multiply(a,5)
# # sess = tf.Session()
# # print(sess.run(b))
# # #定义一个字典，将a的值替换为100
# # dict={a:100}
# # r = sess.run(b,feed_dict=dict)  #返回值为500，而不是30
# #
# # sess.close() #关闭session，以便释放资源"
# # print(r)
#
# weights = tf.Variable(tf.random_normal([784, 200], stddev=0.35), name="weights")
#
# print(weights)


#
# import tensorflow as tf
# graph=tf.Graph()
# with graph.as_default():
#     in_1=tf.placeholder(tf.float32, shape=[], name="input_a")
#     in_2=tf.placeholder(tf.float32, shape=[], name="input_b")
#     const=tf.constant(3, dtype=tf.float32, name="static_value")
#     with tf.name_scope("Transformation"):
#         with tf.name_scope("A"):
#             A_mul=tf.multiply(in_1, const)
#             A_out=tf.subtract(A_mul, in_1)
#         with tf.name_scope("B"):
#             B_mul=tf.multiply(in_2, const)
#             B_out=tf.subtract(B_mul, in_2)
#         with tf.name_scope("C"):
#             C_div=tf.div(A_out, B_out)
#             C_out=tf.add(C_div, const)
#         with tf.name_scope("D"):
#             D_div=tf.div(B_out, A_out)
#             D_out=tf.add(D_div, const)
#             out=tf.maximum(C_out, D_out)
# writer=tf.summary.FileWriter('log', graph=graph)
# writer.close()
'''
import tensorflow as tf
import numpy as np
sess = tf.InteractiveSession()
# 产生一个4x4的矩阵，满足均值为0，标准差为1的正态分布
matrix_input = tf.Variable(tf.random_normal([4,4],mean=0.0, stddev=1.0))
# 对变量初始化，这里对a进行初始化
tf.global_variables_initializer().run()
# 输出原始矩阵的值
print("原始矩阵:\n",matrix_input.eval())
# 对原始矩阵用Relu函数进行激活处理
matrix_output = tf.nn.relu(matrix_input)
# 输出处理后的矩阵的值
print("Relu函数激活后的矩阵:\n",matrix_output.eval())


def sigmoid(x):
    return 1.0/(1+np.exp(-x))
#定义一个5个样本3种分类的问题，且每个样本可以属于多种分类
y = np.array([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[0,1,1]])
logits = np.array([[10,3.8,2],[8,10.9,1],[1,2,7.4],[4.8,6.5,1.2],[3.3,8.8,1.9]])

#按自定义计算公式计算的结果
y_pred = sigmoid(logits)
print('y_pred :',y_pred)
output1 = -y*np.log(y_pred)-(1-y)*np.log(1-y_pred)
print('Self_Define_output1 : ', output1)
with tf.Session() as sess:
  y = np.array(y).astype(np.float64) # labels是float64的数据类型
  #按Tensorflow函数计算结果，与自定义计算公式计算结果相同
  output2 = sess.run(tf.nn.sigmoid_cross_entropy_with_logits(labels=y,logits=logits))
  print('sigmoid_cross_entropy_with_logits : ', output2)
  #调用tf.reduce_mean（） 运算结果的平均值
  reduce_mean = sess.run(tf.reduce_mean(output2))
  print('reduce_mean : ',reduce_mean)
'''
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.python.keras.layers import Input, Dense
from tensorflow.python.keras.models import Model
from tensorflow.examples.tutorials.mnist import input_data
# % matplotlib inline
###########################################################################################################
  # 为避免网络问题，这里我们定义处理本地数据集MNIST的加载函数
# def load_mnist(path, kind='train'):
#     """Load MNIST data from `path`"""
#     labels_path = os.path.join(path, '%s-labels-idx1-ubyte' % kind)
#     images_path = os.path.join(path, '%s-images-idx3-ubyte' % kind)
#
#     with open(labels_path, 'rb') as lbpath:
#       magic, n = struct.unpack('>II', lbpath.read(8))
#       labels = np.fromfile(lbpath, dtype=np.uint8)
#
#     with open(images_path, 'rb') as imgpath:
#       magic, num, rows, cols = struct.unpack(">IIII", imgpath.read(16))
#       images = np.fromfile(imgpath, dtype=np.uint8).reshape(len(labels), 784)
#
#     return images, labels
#
#
# # 读取本地训练数据和测试数据
#
# x_train, y_train = load_mnist('D:/TF/', kind='train')
# x_test, y_test = load_mnist('D:/TF/', kind='t10k')
# print(x_test)
'''
x_train = x_train.reshape(-1, 28, 28, 1).astype('float32')
x_test = x_test.reshape(-1, 28, 28, 1).astype('float32')

# 归一化数据，使之在[0,1] 之间
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.

# 对x_train展平为：-1*784
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))

# 定义输入输入层节点、隐含层节点数
input_img = Input(shape=(784,))
encoding_dim = 32

# 利用keras函数式模型
encoded = Dense(encoding_dim, activation='relu')(input_img)
decoded = Dense(784, activation='sigmoid')(encoded)

# 创建自编码模型
autoencoder = Model(inputs=input_img, outputs=decoded)

# 创建编码器模型
encoder = Model(inputs=input_img, outputs=encoded)

encoded_input = Input(shape=(encoding_dim,))
decoder_layer = autoencoder.layers[-1]

# 创建解码器模型
decoder = Model(inputs=encoded_input, outputs=decoder_layer(encoded_input))

# 编译自编码器模型
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
# 训练该模型
autoencoder.fit(x_train, x_train, epochs=50, batch_size=256,
                  shuffle=True, validation_data=(x_test, x_test))
# 输出预测值
encoded_imgs = encoder.predict(x_test)
decoded_imgs = decoder.predict(encoded_imgs)

# 显示10个数字
n = 10
plt.figure(figsize=(20, 4))
for i in range(n):
  # 可视化输入数据
  ax = plt.subplot(2, n, i + 1)
  plt.imshow(x_test[i].reshape(28, 28))
  plt.gray()
  ax.get_xaxis().set_visible(False)
  ax.get_yaxis().set_visible(False)
  # 可视化自编码器学习的结果
  ax = plt.subplot(2, n, i + 1 + n)
  plt.imshow(decoded_imgs[i].reshape(28, 28))
  plt.gray()
  ax.get_xaxis().set_visible(False)
  ax.get_yaxis().set_visible(False)
plt.show()
'''

labels_path = os.path.join('D:/TF/', 't10k-labels.idx1-ubyte' )
images_path = os.path.join('D:/TF/', 'train-images.idx3-ubyte' )
with open(labels_path, 'rb') as lbpath:
  magic, n = struct.unpack('>II', lbpath.read(8))
  labels = np.fromfile(lbpath, dtype=np.uint8)

with open(images_path, 'rb') as imgpath:
  magic, num, rows, cols = struct.unpack(">IIII", imgpath.read(16))
  print(magic,num,rows,cols)
  images = np.fromfile(imgpath, dtype=np.uint8).reshape(len(labels), 784)

# # labels_path = os.path.join('D:/TF/', 't10k-labels-idx1-ubyte')
# x_train, y_train = load_mnist('D:/TF/', kind='train')
# print(labels_path)
# print(labels)