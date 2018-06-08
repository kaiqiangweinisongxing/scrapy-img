#!/usr/bin/env python 
#-*- coding: utf-8 -*- 

import urllib.request
import gevent 
import re,time
from gevent import monkey 
import json   
import os

#monkey.patch_all() 

def geturllist(url): 
    '''返回目标图片的url列表
    '''
    s = urllib.request.urlopen(url)
    text = s.read().decode('utf-8')                             #以utf-8的格式解码
    s.close()
    html = re.search(r'<ol.*</ol>', text, re.S)                 #正则匹配<ol>标签（内含图片url）,返回匹配到的第一个。re.s：包括换行符在内的任意字符
    
    #另一种正则匹配方法
    #regex = re.compile(r'<ol.*</ol>', re.S)                    
    #html = regex.search(text)
    #print('html.group()：',html.group().encode("utf-8"))       #以utf-8格式查看所有的元素
    
    urls_gif = re.finditer(r'org_src="(.+?)"',html.group(),re.I)   #得到一个callable_iterator。re.i：忽略大小写
    urls_jpg = re.finditer(r'<img src="(.+?)" /></p>',html.group(),re.I)
    url_list=[]
    for i in urls_gif: 
        #group()和group(0)是一样的，得到匹配的所有字符，groups()得到全部正则表达式部分的tuple，group(1)是其中的第一条
        #url="http:"+i.group(1).strip()+str("jpg")
        url="http:"+i.group(1).strip()
        url_list.append(url)
    for i in urls_jpg:
        url="http:"+i.group(1).strip()
        url_list.append(url)
    #time.sleep(1)
    return url_list 
    
def download2(down_url,path): 
    '''用读写二进制文件的方式下载图片
    down_url：图片的下载链接
    path：图片的存放目录
    '''
    fileName=str(time.time())[:-3]+"_"+re.sub('.+/','',downurl)
    pic_response = urllib.request.urlopen(downurl)
    pic_content = pic_response.read()
    with open(path+'\\'+fileName,"wb")  as picFile:
        picFile.write(pic_content)    

def download(down_url): 
    '''接收图片的下载链接，下载并保存到本地,遇到10060错误,改用读写二进制文件的方式下载图片
        down_url : 下载链接
    '''
    name=str(time.time())[:-3]+"_"+re.sub('.+/','',down_url)
    try:
        urllib.request.urlretrieve(down_url, path+"\\"+name)
    except urllib.error.URLError as e:  
        print(e.reason)
    except urllib.error.URLError as e: 
        print(e.reason)  
    #urllib.request.urlretrieve(down_url, path+"\\"+name,schedule)  
'''
def schedule(a,b,c):
    ''''''urlretrieve的回调函数
    a : 已经下载的数据块
    b : 数据块的大小
    c : 远程文件的大小
   ''''''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print('%.2f%%' % per)
 ''' 
def getpageurl(): 
    '''返回目标网页url的列表
    '''
    page_list = [] 
    for page in range(1,5):                                              #对各页进行循环爬取
        url="http://jandan.net/ooxx/page-"+str(page)+"#comments"         #图片所在url 
        page_list.append(url)                                            #把生成的url加入到page_list中
    return page_list 

if __name__ == '__main__': 
    #在当前目录下创建存放图片的文件夹  
    path = os.getcwd()+r'\Image'+str(time.time())           
    if not os.path.exists(path):
        os.mkdir(path)
 
    #获得目标网页的url列表，将列表元素反向
    pageurl = getpageurl()[::-1]

    #进行图片下载  
    jobs = [] 
    count = 0   #图片数量
    for i in pageurl: 
        for (downurl) in geturllist(i): 
            #downurl参数传给download函数，gevent是第三方库，其实是通过greenlet实现协程
            #g = gevent.spawn(download, downurl)     #得到 Greenlet 对象
            #jobs.append(g)  
            print('downloading - %d -: %s'% (count,downurl))
            download2(downurl,path)              #下载图片
            count = count + 1 
    print('The count of images:',count)
    #gevent.joinall(jobs)                        #有漏洞，会执行不下去
    print("Done！")

'''参考文献：
10060错误 : http://blog.csdn.net/wetest_tencent/article/details/51272981
WinError 10054 : http://blog.csdn.net/illegalname/article/details/77164521
正则表达式：http://www.runoob.com/regexp/regexp-syntax.html
urllib.request.urlretrieve  ： http://www.nowamagic.net/academy/detail/1302861
'''