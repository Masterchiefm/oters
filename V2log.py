import re,requests
def openlog(directory):
    #打开日志，将日志转化为字典
    
    log = open(directory,'r')
    
    iplist = []#定义ip列表
    
    records = {}#定义记录字典
    
    def decode(info):
        
        #定义字典，记录ip数，以及访问内容、时间
        result = {'ip':'','site':'','date':''}
        if "accepted" in info:
            #print('accepted')
            pass
        else:
            return 
        
        #开始解析输入的信息：
        date = re.search(r'[0-9].*? [0-9].*? ',info)
        #print(date)
        ip = re.search(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)',info)
        ipv6 = re.search(r"""[0-9a-z]+\:[0-9a-z]+\:[0-9a-z]+\:[0-9a-z]+\:[0-9a-z]+\:[0-9a-z]+\:[0-9a-z]+\:[0-9a-z]+""",info)
        site = re.search(r'[a-z]{1,10}\..*:443',info)
        
        if site == None:
            return 
        
        if ip ==None: #将ipv6地址与ipv4合并
            if ipv6 == None:
                return 
            else:
                ip = ipv6
                
        if date == None:
            return 
        
        result['ip'] = ip.group()
        result['site'] = site.group()
        result['date'] = date.group()
        #print('------------------')
        #print(result)
        return result
        
    for info in log:
        #print (info)
        
        record = decode(info) #读取单行记录
        #print(record)
        
        if record == None:
            continue
       
        if record['ip'] in iplist:
            records[record['ip']].append(record['date']+record['site'])
        else:
            iplist.append(record['ip'])
        
            records[record['ip']]= list()
            records[record['ip']].append(record['date']+record['site'])
            
    return records
            
        
        
def api_locate(ip):
    #输入ip,返回物理地址,使用ip138.com的api，很方便，但是不准。取得的地址不对
    #import re
    location = '0'
    print('locating ',ip,'...')
    i = 0
    while i<3:
        try:
            #http://ip-api.com/json/115.191.200.34?lang=zh-CN
            
            #page= requests.get(('http://apidata.chinaz.com/CallAPI/ip?key=1259c33c50f74cc299afb13ea48efae6&ip=' + ip.strip()))
            url = 'http://ip-api.com/json/' + ip.strip() + '?lang=zh-CN'
            #print(url)
            page = requests.get(url)
            i=6
        except:
            input('继续？')
            i = i + 1
    
    
    result = dict(page.json())
    #print(result)
    location = result['country']+result['regionName']+result['city']
    
    return location   

def locate(ip):
    # 下载站长之家的网页，从网页中提前ip地址。比较准确
    print(ip)
    url="https://ip.tool.chinaz.com/" + ip.strip()
    page = requests.get(url)
    if  re.search(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)',ip):
        print('ipv4')
        all = ''
        for line in page.content.splitlines():
            all = all + line.decode('utf-8').replace('\r\n','').replace(' ','')
        a=str(re.search ('Whwtdhalfw30-0.*?/p',all))
            
        if a:
            try:
                result = str(re.search('p>.*?<',a).group()).replace('p','')
                return result
            except:
                return '未知区域'
        else:
            return '未知区域'
        
        

    elif  re.search(r"""[0-9a-z]+\:[0-9a-z]+\:[0-9a-z]+\:[0-9a-z]+\:[0-9a-z]+\:[0-9a-z]+\:[0-9a-z]+\:[0-9a-z]+""",ip):
        print('ipv6')
        for line in page.content.splitlines():
            if 'Whwtdhalf w54-0' in line.decode('utf-8'):
                try:
                    location0 = str(re.search(r'>.*?<',line.decode('utf-8')).group())
                    if "物理位置" in location0:
                        pass
                    else:
                        location = location0
                        return (location)
                except:
                    return "未知区域"
    else:
        print('wrong ip')
        return 'ip错误'
    
    
if  "main" in __name__:
    #print('ss')
    log = openlog('/var/log/v2ray/access.log')
    #print((log))
    
    #创建记录文件夹
    import time
    import os
    date = time.strftime("%Y-%m-%d", time.localtime())
    path = '''/var/log/v2ray/''' + date + '/c各ip记录'
    if not os.path.exists(path):
        os.makedirs(path)
        
    for ip in log.keys():
        location = locate(ip)
        print(location)
        #为单个ip创建记录文件
        file = open((path + '''/'''  + ip + "--" +location),'a')
        data =log[ip]
        for line in data:
            file.write((line + '\n'))
        file.close  
