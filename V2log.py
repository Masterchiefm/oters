#!/usr/bin/env python
# coding: utf-8

# In[ ]:
print('start sorting v2ray')

def decodelog(info):
    import re
    result = {'ip':'','site':'','date':''}
    if 'accepted' in info:
        pass
    else:
        return 
    date = re.search(r'[0-9].*? [0-9].*? ',info)
    ip = re.search(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)',info)
    site = re.search(r'[a-z]{1,10}\..*:443',info)
    
    if  site == None:
        return 
    if  ip == None:
        return 
    if  date == None:
        return 
    result['ip'] = ip.group()
    result['site'] = site.group()
    result['date'] = date.group()
    return result


# In[ ]:


def locateip(ip):
    ## 直接访问站长之家，获取网页，但是需要proxy，优点：内容较为详细
    #print('locating ',ip,'...')
    import requests
    requests.packages.urllib3.disable_warnings() 
    
    proxy = 'chief:passwd@112.74.105.83:2053'
    proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy,
}
    #proxies={'http':'chief:passwd@112.74.105.83:2053','https':'chief:passwd@112.74.105.83:2053'}
    
    i = 0
    while i < 3:
        try:
            page = requests.get(('https://ip.tool.chinaz.com/'+ip),proxies=proxies,verify=False,timeout=30)
            i = 4
        except:
            i = i + 1
    
    
    for line in page.content.splitlines():
        if 'Whwtdhalf w50-0' in line.decode('utf-8'):
            l = (line.decode('utf-8')).find('>')
            import re
            location = re.search(r'>.*?<',line.decode('utf-8'))
            
    #print(location.group())
    
    return location.group()

from requests import get
from json import loads
def locatip(ip):
    ## 高德地图ip定位api，返回省市（备用，暂时未启用）
    api='''https://restapi.amap.com/v3/ip?key=4de94fb13201c842b74bbc9ab236f7c1&ip=''' + ip 
    location = loads(get(api).content.decode('utf-8'))
    location_info=(location['province']+location['city'])
    return location_info
# In[ ]:


def each_ip_log():
    import time
    import os
    date = time.strftime("%Y-%m-%d", time.localtime())
    path = '''/var/log/v2ray/''' + date + '/a各ip记录'
    if not os.path.exists(path):
        os.makedirs(path)

    for key in log.keys():
        file = open((path + '''/'''  + key),'a')
        data = (log[key])
        for line in data:
            file.write((line + '\n'))
        file.close
    


# In[ ]:


def ip_log():
    import time
    import os
    date = time.strftime("%Y-%m-%d", time.localtime())
    path = '''/var/log/v2ray/''' + date
    if not os.path.exists(path):
        os.makedirs(path)
    file = open((path + '''/''' + 'b来访ip'),'a')
    for key in log.keys():
        file.write((key + '\n'))
        file.close


# In[ ]:


log = open('/var/log/v2ray/access.log','r')
iplist = []
records = {}
for info in log:
    record = decodelog(info)
    
    if record == None:
        continue
       
    if record['ip'] in iplist:
        records[record['ip']].append(record['date']+record['site'])
    else:
        iplist.append(record['ip'])
        
        records[record['ip']]= list()
        records[record['ip']].append(record['date']+record['site'])

log = {}        
for key in records.keys():
    #print(key)
    log[key + locateip(key)] = records[key]


# In[ ]:


each_ip_log()


# In[ ]:


ip_log()

