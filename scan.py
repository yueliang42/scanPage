#!/usr/bin/env python 
# -*- coding: utf8 -*-
import os
import sys
import httplib2
import threading
import time

sys.path.append('/home/lyue/scanTool/httplib2-master/build/lib')

global http
global fp
global fpPage
global fpWritePage
global fpWritePath
global pageLists

mutexPath = threading.Lock()
mutexPage = threading.Lock()

class myThread(threading.Thread):
        def __init__(self, func, args, name=''):
                threading.Thread.__init__(self)
                self.func = func
                self.args = args
                self.name = name 

        def  run(self):
                print 'line 28'
                apply(self.func, self.args)

def scanPagePath(host,path,page,nonPathPageStatus):
        global http
        global fpWritePage
        
        page = page.strip('\n')
        print '37' + host + path + page
        response,content= http.request(host + path + page, 'GET')
        print 'line 38 ' + str(response)
        if response.status != nonPathPageStatus.status or (response['content-length'] != nonPathPageStatus['content-length'] and response.status != 404 ):
                time.sleep(1)
                existsPage = path + page
                mutexPage.acquire()
                fpWritePage.write(existsPage)
                fpWritePage.write('\n')
                mutexPage.release()
        else :
                pass

def scanPath(host,path,nonPathStatus,nonPathPageStatus):
        global http
        global fpPage
        global fpPage
        global fpWritePath
        global fpWritePage
        global pages
        

        path = path.strip('\n')
        print 'line 58 %s' % path
        response,content= http.request(host + path , 'GET')
        print 'line 60 ' + str(response)
        if  response.status != nonPathStatus.status or ( response['content-length'] != nonPathStatus['content-length'] and response.status  != 404) :
                time.sleep(1)
                existsPath = path
                mutexPath.acquire()
                fpWritePath.write(existsPath)
                fpWritePath.write('\n')
                mutexPath.release()
                for page in pages:
                        scanPagePath(host, existsPath, page, nonPathPageStatus)
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
                print('example:' + 'sys.argv[0]' + 'http://www.njupt.edu.cn ' + 'php/asp/html')
                sys.exit(0)
        host = sys.argv[1]
        page = sys.argv[2]
        print(host)
        print page

        http = httplib2.Http('.cache')
#        response,content = http.request(host)
        response,content = http.request(host + '/mustnotexistsppath')
        nonPathStatus = response

        response,content = http.request(host + '/mustnotexistsppath/' + page )
        nonPathPageStatus = response
        
        fp = open('path.txt', 'r')
        paths = fp.readlines()
        print len(paths)

        fpPage = open('page.txt', 'r')
        pages = fpPage.readlines()


        fpWritePath = open('resultsPath.txt', 'w')
        fpWritePage = open('resultsPage.txt', 'w')
        
        threads = []
        max = len(paths)

        for i in range(0, max):
                t = myThread(scanPath, (host, paths[i], nonPathStatus, nonPathPageStatus), scanPath.__name__)
                threads.append(t)

        for i in range(0,max):
                threads[i].setDaemon(True)
                threads[i].start()

        for i in range(0,max):
                threads[i].join()# join means wait until the child thread run over ,then the main thread start continue run
                
        fp.close()
        fpPage.close()
        fpWritePage.close()
        fpWritePath.close()

main()
