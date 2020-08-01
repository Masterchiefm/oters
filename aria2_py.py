#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json, requests, os,re
from requests import get

global token

global rpc
rpc = input('Please input RPC:\n')
if rpc == '':
    rpc = 'http://127.0.0.1:6800/jsonrpc'
    
token=input('Please input token:\n')
token='token:'+token.strip()
global path
path = input('input path:\n')
# In[ ]:


def rpc_download_url(url,path,title):
    Dir = path + "/" + title
    '''输入下载链接或者Magnet链接，然后添加下载任务。'''
    jsonreq=json.dumps({'jsonrpc':'2.0',
                'id':'1',
                   'method' : 'aria2.addUri',
                   'params':[token,[url],{"dir":Dir}]})
    #print(jsonreq)
    c=requests.post(rpc,data=jsonreq)
    print(c.content)


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
            #print ("getting page ",head)
            picture = download(pic,file_path)
            
            creat_file(title,magnet,path)
            
            
            with open(file_path, 'wb') as file:
                try:
                    file.write(picture.content)
                except:
                    print('pic error')
        rpc_download_url(magnet,path,title)


# In[ ]:


def creat_file(title,magnet,path):
    if not os.path.exists(str(path)):
        os.makedirs(str(path))   
        #创建页文件夹下的分文件夹
    if not os.path.exists((path) + "/" + title):
        os.makedirs((path) + "/" +  title)
        
    index = """  <?php
function fileShow($dir, &$fileArr=array()){ 
    $handle = opendir('./');
    while($file = readdir($handle)){
        if($file !== '..' && $file !== '.'){
            $f = $dir.'/'.$file;
            if(is_file($f)){
                {
                $temp = explode('.',$file); 
                $fileArr['type'][] = $temp[1]; 
                //$fileArr['name']保存图片名称
                $fileArr['name'][] = $temp[0];       
                  
                //$fileArr['path']保存图片路径       
                $fileArr['path'][] = $dir.'/'.$file;
}
            }
            else{
                fileShow($f, $fileArr);
            }
        }  
    }
    return $fileArr;
}
 
$imgs = fileShow('./'); //$一个文件夹目录，目录内是jpg图片

asort($imgs['name'], 1);         //保持索引关系把值按数字处理进行升序
foreach($imgs['name'] as $k=>$name)
{
    if( $imgs['type'][$k] == 'jpg'){
    echo $name.$imgs['type'][$k].'<br />';
    echo '<img style="width:1000px;" src="'.$imgs['path'][$k].'" />';
}
}

    """ 
    index = index + """echo '<br>""" + magnet + "'?>"

    index_file = path + '/' + title + "/" + "index.php"
    #rpc_download_url(magnet,path)
    with open(index_file,'w',encoding = 'utf-8') as w_file:
        for each_line in index:
            w_file.write(each_line)


# In[ ]:


def aria2_remove(gid):
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
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
                print(directory,'download complet')
                downloads[directory]=gid
        else:
            print(directory,'downloading')
    return downloads


# In[ ]:


def menu():
    
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
                cmd = 'rclone move '  + dir + ' gdrive:' + dir + ' -P'
                sleep(60)
                os.system(cmd)
                
                
                
                aria2_remove(file[key])
                #os.system(cmd2)
                
            sleep(30)
    elif opt == '4':
        path = input('input saving path:\n')
        folder = input('input saving folder:\n')
        
        url = input('input url/magnet:\n')
        rpc_download_url(url,path,folder)
    elif opt == '0':
        return 0 
    else:
        print('输入有误')
        return 1
    return 1
    
        


# In[ ]:







# In[ ]:

if __name__ == "__main__":
    a=1
    while a:
        a = menu()
