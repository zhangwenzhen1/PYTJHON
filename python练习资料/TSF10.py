import matplotlib.pyplot as plt
import tensorflow as tf
import os
from PIL import Image #处理图像的包
import numpy as np
'''
image_raw_data_jpg = tf.gfile.FastGFile('D:/image/cat/cat.jpg', 'rb').read()

with tf.Session() as sess:
    img_data = tf.image.decode_jpeg(image_raw_data_jpg)  # 图像解码

    plt.figure(1)  # 图像显示
    print(sess.run(img_data))  # 显示图像矩阵
    plt.imshow(img_data.eval())  # 显示图像
    plt.show()
'''
#########################################################################
'''
path = 'D:/image/cat/cat.jpg'
file_queue = tf.train.string_input_producer([path])  # 创建输入队列
image_reader = tf.WholeFileReader()
_, image = image_reader.read(file_queue)
image = tf.image.decode_jpeg(image)

with tf.Session() as sess:
    coord = tf.train.Coordinator()  # 协同启动的线程
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)  # 启动线程运行队列
    print(sess.run(image))
    plt.figure(1)  # 图像显示
    plt.imshow(image.eval())  # 显示图像
    plt.show()
    coord.request_stop()  # 停止所有的线程
    coord.join(threads)
'''
###################################################################
folder = 'D:/image/'
#设定图像类别标签标签，标签名称和对应子目录名相同
label = {'cat','dog'}
#要生成的文件
writer = tf.python_io.TFRecordWriter(folder+'cat_dog.tfrecords')
#记录图像的个数
count=0
for index,name in enumerate(label):
    folder_path=folder+name+'/'
    for img_name in os.listdir(folder_path):
        img_path = folder_path+img_name #每一个图片的完整访问路径
        img = Image.open(img_path)
        img = img.resize((128,128))
        img_raw = img.tobytes()#将图片转化为二进制格式
        example = tf.train.Example(features=tf.train.Features(feature={
            "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[index])),
            'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
        })) #example对象对label和image数据进行封装
        writer.write(example.SerializeToString())  #序列化为字符串
        count = count+1
writer.close()