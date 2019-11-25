import csv
import random
import time
import socket
import http.client
# import urllib.request
from bs4 import BeautifulSoup
import requests
# import urllib2
import json
url ='https://restapi.amap.com/v3/geocode/regeo?key=e96f9a501924b3475e1e9335477e8083&location=116.397499,39.908722|116.480881,39.989410&batch=true'
timeout = random.choice(range(80, 180))
rep = requests.get(url,timeout = timeout)
rep.encoding = 'utf-8'
hjson = json.loads(rep.text)
print(rep.text)

pure_json = rep.text[rep.text.index('[') + 2: rep.text.rindex(']')]

print('12:',pure_json)
# dealers = json.loads(pure_json)
# print(dealers.keys())
# print(rep.text)
# print(type(hjson))
# print(hjson['regeocode']['formatted_address'])
# print(hjson['regeocode']['formatted_address'])
# print(hjson)

for key,value in hjson.items():
    if key =='regeocodes':
        # print(value[0])
        for i in value:
            for k,v in i.items():
                if k=='addressComponent':
                    # print(v)
                    for m,n in v.items():
                        if m=='district':
                            print(n)