# - * - coding: utf - 8 -
# *-
"""
Created on Fri Aug 15 10:06:16 2018
@author: zjp
Python3.6.6
"""

# 加载必要的包

import csv
import json
import time
import requests
from bs4 import BeautifulSoup

origin_path = 'E://GetRoute/HuaNan/中文地址.csv'  # 原始数据文件路径
new_path = 'E://GetRoute/HuaNan/地址对应坐标.txt'  # 爬取数据文件保存路径

url_geocode = r'http://api.map.baidu.com/geocoder/v2/?'  # 百度地图api网址
AK = ['oFCSeioUzdN5NfzSlBBXqBEfXgp26mGM', 'Akqk5xjbSGzy1WC1IUF04K2CQWGtOFNv', 'HCdq1Ry35rwgVQwjAXqAEQGzWNY7pi1h',
      'GtOZERwlG0PynPwFrBYaF9wWcAGxvaw8', 'iRKkZehZimIWdGoxfjlbtLrYb0VVgVaD', 'gG0KIBhAGpAVvaRUlwFjmOtsTKGRK2tf',
      'CSsyosiklqyYUDNnBP0BR63fa9BzCHFf', 'mq4TZshHveVqML3icCC6AWnS25rbjYBz', 'rBYetA6WQNOlXtQWInz8ckRE0iCDsUjB',
      'QUshHD8KUAk8y9gLwDhQ6RyOgQxEB8VD', '7Ict6oZmpAYYXMjha2Tk5g4ENTCYwx03']  # 开发者应用密钥
cod = r'&ret_coordtype=bd09ll'  # 坐标类型(设置为百度坐标)
machine_data = csv.reader(open(origin_path, 'r', encoding='utf-8'))  # 读取原始文件数据
n = 0
akn = 0
column_names = '设备序列号 取点方式1 准确度1 网点纬度 网点经度 网点名称 取点方式2 准确度2 安装地址纬度 安装地址经度 安装地址 取点 准确度 最佳纬度 最佳经度 安装方式 最佳地址'
with open(new_path, 'a', encoding='utf-8') as f:  # 把变量名写入新文件
    f.write(column_names)
    f.write('\n')
    f.close()
while True:
    try:
        for addr in machine_data:  # 循环爬取每一条数据
            province = str(addr[0])  # 省份
            city = str(addr[1])  # 城市
            mac = str(addr[2])  # 设备序列号
            wd = str(addr[3])  # 网点名称
            anz = str(addr[4])  # 安装地址
            anz_type = str(addr[5])  # 安装类型
            add1 = province + city + wd
            add2 = province + city + anz
            if akn < len(AK):  # AK配额还没用完时
                n += 1
                aknd = AK[akn]  # 第akn个秘钥是aknd
                ak = r'&output=json&ak=' + aknd
                address1 = r'address=' + add1
                tar_url = url_geocode + address1 + ak + cod  # 最终url网址
                response = requests.get(url=tar_url)  # 请求网址响应
                soup = BeautifulSoup(response.content, 'html.parser')  # 解析网页内容
                response.close()  # 获取内容后关闭网页(防止被远程主机认定为攻击行为)
                dictinfo = json.loads(str(soup))  # json数据转dict数据
                status = dictinfo['status']
                print(status)
                if status == 0:  # status状态码为0表示服务器响应成功,本次循环爬取数据成功
                    lng1 = round(dictinfo['result']['location']['lng'], 8)  # 经度保留8位数
                    lat1 = round(dictinfo['result']['location']['lat'], 8)  # 纬度保留8位数
                    precise1 = dictinfo['result']['precise']  # 1为精准打点,可靠性高;0为模糊打点,准确性低
                    confidence1 = dictinfo['result']['confidence']  # 可信度,描述打点准确度,大于80表示误差小于100m
                    geocode1 = str(precise1) + ' ' + str(confidence1) + ' ' + str(lat1) + ' ' + str(lng1) + ' ' + add1
                elif status == 302 or status == 210:  # 302 配额超限,限制访问;210 IP验证未通过，则使用下一个Ak
                    akn += 1
                    lat1 = 'break'
                    lng1 = 'break'
                    precise1 = 0
                    confidence1 = 0
                    geocode1 = '0 0 break break ' + add1
                else:
                    lat1 = 'na'
                    lng1 = 'na'
                    precise1 = 0
                    confidence1 = 0
                    geocode1 = '0 0 na na ' + add1
                address2 = r'address=' + add2
                tar_url2 = url_geocode + address2 + ak + cod  # 总的url
                response2 = requests.get(url=tar_url2)  # 请求网址响应
                soup2 = BeautifulSoup(response2.content, 'html.parser')  # 解析内容
                response2.close()  # 获取内容后关闭网页(防止被远程主机认定为攻击行为)
                dictinfo2 = json.loads(str(soup2))  # json转dict
                status2 = dictinfo2['status']
                print(status2)
                if status2 == 0:
                    lng2 = round(dictinfo2['result']['location']['lng'], 8)  # 经度保留8位数
                    lat2 = round(dictinfo2['result']['location']['lat'], 8)  # 纬度保留8位数
                    precise2 = dictinfo2['result']['precise']  # 1为精准打点，可靠性高；0为模糊打点，准确性低
                    confidence2 = dictinfo2['result']['confidence']  # 可信度,描述打点准确度,大于80表示误差小于100m
                    geocode2 = str(precise2) + ' ' + str(confidence2) + ' ' + str(lat2) + ' ' + str(lng2) + ' ' + add2
                elif status2 == 302 or status2 == 210:  # 配额超限,限制访问;IP验证未通过
                    akn += 1
                    precise2 = 0
                    confidence2 = 0
                    lat2 = 'break'
                    lng2 = 'break'
                    geocode2 = '0 0 break break ' + add2
                else:
                    lat2 = 'na'
                    lng2 = 'na'
                    precise2 = 0
                    confidence2 = 0
                    geocode2 = '0 0 na na ' + add2
                if anz_type == '在行':
                    if precise1 == 1:
                        geocode3 = str(precise1) + ' ' + str(confidence1) + ' ' + str(lat1) + ' ' + str(
                            lng1) + ' ' + anz_type + ' 网点'
                    elif precise1 == 0 and precise2 == 0:
                        geocode3 = str(precise1) + ' ' + str(confidence1) + ' ' + str(lat1) + ' ' + str(
                            lng1) + ' ' + anz_type + ' 网点'
                    else:
                        geocode3 = str(precise2) + ' ' + str(confidence2) + ' ' + str(lat2) + ' ' + str(
                            lng2) + ' ' + anz_type + ' 安装地址'
                else:
                    geocode3 = str(precise2) + ' ' + str(confidence2) + ' ' + str(lat2) + ' ' + str(
                        lng2) + ' ' + anz_type + ' 安装地址'
                geocode = mac + ' ' + geocode1 + ' ' + geocode2 + ' ' + geocode3
                with open(new_path, 'a', encoding='utf-8') as f:
                    f.write(geocode)
                    f.write('\n')
                    f.close()
                print('good' + str(n))
            else:
                print('配额不足！')
                break  # 配额不足中断整个循环
        print('已完成')
    except:  # 发生错误时执行以下代码块
        print('未知错误')
        time.sleep(5)
        with open(new_path, 'a', encoding='utf-8') as f:
            f.write('未知错误')
            f.write('\n')
            f.close()
        continue  # 发生未知错误跳过该次循环
    print('程序已停止')
    break
