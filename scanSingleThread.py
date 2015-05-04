#!/usr/bin/env python 
# -*- coding: utf8 -*-
import os
import sys
import httplib2
sys.path.append('/home/lyue/scanTool/httplib2-master/build/lib')

global http
global fp
global fpPage
global fpWritePage
global fpWritePath
global pageLists


def scanPagePath(host,path,page,nonPathPageStatus):
        global http
        global fpWritePage
        
        page = page.strip('\n')
        print 'line 21 url is :' + host + path + page
        response,content= http.request(host + path + page, 'GET')
        print 'line 23 :' + str(type(response))
        print nonPathPageStatus.status
        print type(nonPathPageStatus)
        print response.status
        print type(response.status)
        print content

        if response.status != nonPathPageStatus.status or (response['content-length'] != nonPathPageStatus['content-length'] and response.status != 404 ):
                existsPage = path + page
                print 'line 25'
                print existsPage
                fpWritePage.write(existsPage)
                fpWritePage.write('\n')
        else :
                pass

def scanPath(host,paths,nonPathStatus,nonPathPageStatus):
        global http
        global fpPage
        global fpPage
        global fpWritePath
        global fpWritePage
        global pages
        print 'line 37'
        print pages

        hostlyue = host
        if len(paths) == 0 :
                print paths
                print 'paths is null,wrong'
                sys.exit(0)
        else :
                for path in paths:
                        print 'line 50 ' + path
                        path = path.strip('\n')
                        print 'line 52 :' + host + path
                        response,content= http.request(host + path , 'GET')
                        print 'line 54 : response' + str(type(response))
                        print nonPathStatus.status
                        print response.status
                        print nonPathStatus
                        print response
                        print path
                        if  response.status != nonPathStatus.status or ( response['content-length'] != nonPathStatus['content-length'] and response.status  != 404) :
                                existsPath = path
                                print 'line 57: ' + existsPath
                                fpWritePath.write(existsPath)
                                fpWritePath.write('\n')
                                print 'line 60'
                                print 'line 61 :' + str(pages)
                                for page in pages:
                                        scanPagePath(hostlyue, existsPath, page, nonPathPageStatus)
                        else : 
                                pass
def main():
        global http
        global fpPage
        global fpPage
        global fpWritePath
        global fpWritePage
        global pages

        if len(sys.argv) < 3:
                print('args must = 3')
                print('usage:' + sys.argv[0] + 'host' + '.ext')
                print('example:' + 'sys.argv[0]' + 'http://www.njupt.edu.cn' + 'php/asp/html')
                sys.exit(0)
        host = sys.argv[1]
        page = sys.argv[2]
        print(host)

        http = httplib2.Http('.cache')
#        response,content = http.request(host)
        response,content = http.request(host + '/mustnotexistsppath')
        nonPathStatus = response

        response,content = http.request(host + '/mustnotexistsppath/' + page )
        nonPathPageStatus = response
        
        fp = open('path.txt', 'r')
        paths = fp.readlines()

        fpPage = open('page.txt', 'r')
        pages = fpPage.readlines()

        print 'line 95'
        print pages

        fpWritePath = open('resultsPath.txt', 'w')
        fpWritePage = open('resultsPage.txt', 'w')



        scanPath(host, paths, nonPathStatus, nonPathPageStatus)

        fp.close()
        fpPage.close()
        fpWritePage.close()
        fpWritePath.close()

main()
