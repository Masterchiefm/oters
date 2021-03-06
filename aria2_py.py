#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json, requests, os,re,urllib
from requests import get
from time import sleep

global token

global rpc
rpc = input('Please input RPC:\n')
if rpc == '':
    rpc = 'http://127.0.0.1:6800/jsonrpc'
    
token=input('Please input token:\n')
token='token:'+token.strip()
global path
path = input('input path:\n')
if path[0]:
    pass
else:
    path='/tmp'
if path[0]=='/':
    pass
else:
    path='/'+path


# In[ ]:


def aria2_addUri(url,path,title):
    Dir = path + "/" + title
    '''输入下载链接或者Magnet链接，然后添加下载任务。'''
    jsonreq=json.dumps({'jsonrpc':'2.0',
                'id':'addUri',
                   'method' : 'aria2.addUri',
                   'params':[token,[url],{"dir":Dir}]})
    #print(jsonreq)
    c=requests.post(rpc,data=jsonreq)
    result = c.json()
    return result


# In[ ]:



import os

# 下载部分，下载网页或者图片
def download(url,Type):
    content = ''
    t = 0
    while t < 3:
        try:
            content = get(url,timeout=20)
            if Type == '':
                pass
            else:
                print('获取',Type,'成功')
                
            return content
            t = 4
        except Exception as e:
            t = t + 1
            print('错误，',e)
            content='no picture'
    return content
            


# In[3]:



# 获取图片md链接
def addReadme(gid):
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                          'method':'aria2.getFiles',
                          'params':[token,gid]})
    c = requests.post(rpc,data=jsonreq)
    d=c.json()
    e = d['result']
    print(e)
    Dir  = re.search(r"path\': \'/.*?\.jpg",str(e))
    #print('1',Dir)
    #print(Dir)
    newDir = ''
    try:
        Dir = Dir.group()
        Dir = (Dir).replace("path': '",'')
        newDir = urllib.parse.quote(Dir)
    except:
        print('eee')
    
    md = "\n![](" + newDir + ")"
    return md

# 获取分页数以及每个分页的链接,然后
def get_page_info():
    
    status = True
    urls=[]
    while status:
        # 读取每页的页面链接
        url = input('添加网址链接,exit终止输入：\n')
        if url == 'exit':
            status = 0
        else:
            urls.append(url)
        # 扫描该分页下该标题内的图片信息
        
        
        
    for url in urls:
        pics = []
        mds = []
        magnet = ''
        for line in (download(url,'').content.decode('utf-8').splitlines()):
            # 标题
            if '<meta name="keywords" content=' in line:
                l = line.find("content=") + 9
                rest = line[l:]
                r = rest.find('"')
                title = rest[:r]
                print("\n"+"#####"+title+"#####")
               # 获取所有的图片链接
            elif "img id" in line:
                import re
                p = [m.start() for m in re.finditer('http', line)]
                for l in p:
                    rest = line[l:]
                    r = rest.find('"')
                    pic = rest[:r]
                    if pics != []:
                        if pic != pics[-1]:
                            pics.append(pic)
                    else:
                        pics.append(pic)
                # 获取磁力链接
            elif "magnet:?xt=" in line:
                #print(line)
                l = line.find('magnet:?')
                rest = line[l:]
                r = rest.find('''<''')
                magnet = rest[:r]
                print(magnet)
                
            #print(pics)
                
        i = 0
        print('共',len(pics),'图')
        for pic in pics:
            i = i + 1
            file_path = path + "/" + title + "/" + str(i) + '.jpg'
            ndir = urllib.parse.quote(file_path)
            md = "\n![](" + ndir  + ")"
            mds.append(md)
            #print ("getting page ",head)
            picture = download(pic,file_path)
            if not os.path.exists(str(path)):
                os.makedirs(str(path))   
                #创建页文件夹下的分文件夹
            if not os.path.exists((path) + "/" + title):
                os.makedirs((path) + "/" +  title)
            with open(file_path, 'wb') as file:
                try:
                    file.write(picture.content)
                except:
                    print('pic error')

            
        print('adding file')
        aria2_addUri(magnet,path,title)
        creat_file(title,magnet,path,mds)
        


# In[ ]:


def creat_file(title,magnet,path,mds):
    if not os.path.exists(str(path)):
        os.makedirs(str(path))   
        #创建页文件夹下的分文件夹
    if not os.path.exists((path) + "/" + title):
        os.makedirs((path) + "/" +  title)
        
    index = """bt: """ 
    index = index + magnet + '\n'
    for md in mds:
        index = index + md

    index_file = path + '/' + title + "/" + "README.md"
    
    with open(index_file,'w',encoding = 'utf-8') as w_file:
        for each_line in index:
            w_file.write(each_line)


# In[ ]:


def aria2_remove(gid):
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'remove',
                          'method':'aria2.remove',
                          'params':[token,gid]})
    c=requests.post(rpc,data=jsonreq)
    print(c.content)


# In[115]:


def aria2_tellActive():
    downloads={}
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                          'method':'aria2.tellActive',
                          'params':[token]})
    c=(requests.post(rpc,data=jsonreq)).content
    a=json.loads(c.decode('utf-8'))
    b=a['result']
    #print(c.content)
    for info in b:
        complet_lenth = re.search(r"completedLength\'\: \'[0-9]*",str(info))
        complet_lenth = complet_lenth.group()
        complet_lenth = complet_lenth.replace("completedLength': '",'')
        total_lenth = re.search(r"totalLength\'\: \'[0-9]*",str(info))
        total_lenth = total_lenth.group()
        total_lenth = total_lenth.replace("totalLength': '",'')
        directory = re.search(r"dir\'\: \'.*?,",str(info))
        directory = directory.group()
        directory = directory.replace("dir': '","").replace("',",'')
        gid = re.search(r"gid\'\: \'[a-zA-Z0-9]*",str(info))
        gid = gid.group()
        gid = gid.replace("gid': '","")
        #print(complet_lenth)
        #print(total_lenth)
        if total_lenth == complet_lenth:
            if (int(complet_lenth) > 536870912):
                print('@',directory,'download complet')
                downloads[directory]=gid
                
      
                
        else:
            percent = (int(complet_lenth)/int(total_lenth)) * 100
            print( int(percent),'%',directory)
    return downloads


# In[ ]:


def menu(path):
    
    print('''-----------自动下片机------------''')
    print('''- 1. 添加se网址链接''')
    print('''- 2. 检测状态''')
    print('''- 3. 使用rclone上传已完成任务''')
    print('''- 4. 添加正常下载链接''')
    print('''- 0. 退出''')
    print('''--------------------------------''')
    opt = str(input ('输入选项：'))
    if opt == '1':
        get_page_info()
    elif opt == '2':
        aria2_tellActive()
    elif opt == '3':
        count = 0
        while True:
            from time import sleep
            
            os.system('date')
            file = aria2_tellActive()
            for key in file.keys():
                dir = key.strip()
                if ' ' in dir:
                    dir = dir.replace(' ','''\ ''')
                
                if dir[0] == '/':
                    pass
                else:
                    dir = '/' + dir
                print('---------------------------------------------------')
                print('Preparing to upload ',dir)
                
                
                    
                cmd0 = 'rclone copy '  + dir + ' gdrive:' + dir + ' -P'
                cmd = 'rclone move '  + dir + ' bcgdrive:' + dir + ' -P'
                sleep(30)
                os.system(cmd0)
                os.system(cmd)
                log = open('/tmp/uploadlog','a')
                log.write(dir+'\n')
                log.close
                
                
                
                
                aria2_remove(file[key])
                #os.system(cmd2)
                
            sleep(30)
            count = count + 1
            if count == 10:
                count = 0
                print("sync other clouds")
                #os.system("""rclone sync gdrive:/ bcgdrive:/ -P""")
                os.system("""rclone copy gdrive:/ hell:/ -P""")
                
    elif opt == '4':
        path = input('input saving path:\n')
        folder = input('input saving folder:\n')
        
        url = input('input url/magnet:\n')
        aria2_addUri(url,path,folder)
    elif opt == '0':
        return 0 
    else:
        print('输入有误')
        return 1
    return 1
    
        










# In[ ]:

if __name__ == "__main__":
    a=1
    while a:
        a = menu(path)
