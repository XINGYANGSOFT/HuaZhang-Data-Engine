# -*- coding:utf-8 -*-
import urllib
import urllib.request
import json
import django.utils.http
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from operator import itemgetter  # 排序
import time
from django.core.paginator import Paginator

servers = ['127.0.0.1:8100', '127.0.0.1:8100', '127.0.0.1:8100']  # 多台server的IP

results = []
servernum = len(servers)  # 计算服务器数量，下一版本统计在线数据库数量
resultsnumbers = 0
for server in servers:
    url = 'http://{}/?s={}&j=1&sort=date_modified&ascending=0&date_modified_column=1&path_column=1&c=1000'.format(
        server, '1')
    username = '59'     # 登录everthing服务器 start
    password = '119119'
    p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, url, username, password)
    handler = urllib.request.HTTPBasicAuthHandler(p)
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)  # 登录everthing服务器 end
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))
    resultsnumbers = resultsnumbers + int(data['totalResults'])
    for results_dic in data['results']:
        date_modified = results_dic['date_modified']  # FileTime
        date_modified = int(date_modified[:-7]) - 11644473600  # FileTime to UnixTime
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date_modified))
        results_dic['date_modified'] = date
        results_dic['ip'] = server[:-5]  # 在返回的字典中添加ip去掉端口号
        results_dic['ip_all'] = server
    results.extend(data['results'])
    p = Paginator(results, 5)  # 每页显示5个list的内容
    page1 = p.page(1)   # 第一页
print(page1.object_list)