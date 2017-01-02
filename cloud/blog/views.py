# -*- coding:utf-8 -*-
import urllib
import urllib.request
import json
import django.utils.http
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from operator import itemgetter  # 排序
import time

servers = ['127.0.0.1:8100', '127.0.0.1:8100', '127.0.0.1:8100']  # 多台server的IP

def searchfile(keyword):

    results = []
    servernum = len(servers)  # 计算服务器数量，下一版本统计在线数据库数量
    resultsnumbers = 0
    for server in servers:
        try:
            url = 'http://{}/?s={}&j=1&sort=date_modified&ascending=0&date_modified_column=1&path_column=1&c=1000'.format(
                server, keyword)
            username = '59'     # 登录everthing服务器 start
            password = '119119'
            p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            p.add_password(None, url, username, password)
            handler = urllib.request.HTTPBasicAuthHandler(p)
            opener = urllib.request.build_opener(handler)
            urllib.request.install_opener(opener)  # 登录everthing服务器 end
            response = urllib.request.urlopen(url)
            data = json.loads(response.read().decode("utf-8"))
            resultsnumbers = resultsnumbers + int(data['totalResults'])   # 计算搜索总数量
            for results_dic in data['results']:
                date_modified = results_dic['date_modified']  # FileTime
                date_modified = int(date_modified[:-7]) - 11644473600  # FileTime to UnixTime
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date_modified))
                results_dic['date_modified'] = date
                results_dic['ip'] = server[:-5]  # 在返回的字典中添加ip去掉端口号
                results_dic['ip_all'] = server
            results.extend(data['results'])  # 多台服务器数据合并list
            urllib.request.urlopen(url).close()
        except:
            pass
    return results, servernum, resultsnumbers

def search(request):
    keyword = request.GET.get('k')  # 传入参数关键词
    sort = request.GET.get('s')  # 传入参数排序方式
    if sort == 'date_modified':  # 检查传入sort的参数正确性
        sort = 'date_modified'
    elif sort == 'name':
        sort = 'name'
    elif sort == 'path':
        sort = 'path'
    else:
        sort = 'date_modified'
    if keyword != '':
        results, servernum, resultsnumbers = searchfile(django.utils.http.urlquote(keyword))
        results = sorted(results, key=itemgetter(sort))  # 按照字典的 sort方法排序
        results = results[::-1]  # 倒序排列
        results = results[0:199]  # 取前200个结果，分页
        return render_to_response('search.html', {'title': keyword, 'results': results, 'servernum': servernum, 'resultsnumbers': resultsnumbers})
    else:
        return HttpResponseRedirect('..')  # 如果关键字为空返回主页

def index(request):
    return render_to_response('index.html')

def onlineservers(request):  # everthing 服务器需要能返回网页才可以测试成功
    onlineservers = {}
    for server in servers:
        server = onlineservers['server']
        try:
            url = 'http://{}/'.format(server)
            urllib.request.urlopen(url)
            onlineservers['status'] = '1'
        except:
            onlineservers['status'] = '0'
    return render_to_response('onlineservers.html', {'servers': servers, 'status': status})


