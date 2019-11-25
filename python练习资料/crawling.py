# import urllib.request
# from urllib.error import URLError,HTTPError,ContentTooShortError
# import re
#
# def download(url,user_agent='wswp',num_retries=2,charset='utf-8'):
#     # return urllib.request.urlopen(url).read()
#     print('Downloading：', url)
#     request = urllib.request.Request(url)
#     request.add_header('User-agent',user_agent)
#     try:
#         # html = urllib.request.urlopen(request).read()
#         resp = urllib.request.urlopen(request)
#         cs = resp.headers.get_content_charset()
#         if not cs:
#             cs = charset
#         html =resp.read().decode(cs)
#     except (URLError,HTTPError,ContentTooShortError) as e:
#         print('Download error:', e.reason)
#         html = None
#         if num_retries>0:
#             if hasattr(e,'coad') and 500 <= e.coad <600:
#                 #若返回5XX错误(服务器错误)可重新下载
#                 return download(url,num_retries - 1)
#         return html
#
#
# def crawl_sitemap(url):
#     sitemap = download(url)
#     links = re.findall('<loc>(.*?)</loc>',sitemap)
#     for link in links:
#         html = download(link)
# # print(download('http://meetup.com'))
#
# crawl_sitemap('http://www.runoob.com/python/python-modules.html')

import csv
import json
import requests


url = 'https://c2b-services.bmw.com/c2b-localsearch/services/api/v3/clients/BMWDIGITAL_DLO/DE/pois?country=DE&category=BM&maxResults=%d&language=en&lat=52.507537768880056&lng=13.425269635701511'
jsonp = requests.get(url % 1000)
pure_json = jsonp.text[jsonp.text.index('(') + 1: jsonp.text.rindex(')')]
dealers = json.loads(pure_json)
print(pure_json)
print(dealers.keys())
print(dealers['count'])
print(dealers['data']['pois'][0])

# with open('bmw.csv', 'w',encoding='utf-8') as fp:
#     writer = csv.writer(fp)
#     writer.writerow(['Name', 'Latitude', 'Longitude'])
#     for dealer in dealers['data']['pois']:
#         name = dealer['name']
#         lat, lng = dealer['lat'], dealer['lng']
#         writer.writerow([name, lat, lng])