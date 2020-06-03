#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 看看你能不能坚持15天！


# In[2]:


import time
import os
os.system('clear')
# In[3]:


def read_record():
    
    record = 'Record'
    if os.path.exists(record):
        #print('记录文件存在')
        file = open(record,'r')
    else:
        print('记录文件不存在,为你创建新纪录')
        file = open(record,'w')
        data = 'start_time=' + str(int(time.time())) + "|statu=progressing" + "|end_time="
        file.write(data)
        file.close
        file = open(record,'r')
    origin_data = file.read()
    file.close
    
    l1=origin_data.find('=') + 1
    r1=origin_data.find('|')
    start_time=origin_data[l1:r1]
    
    rest1=origin_data[r1+1:]
    #print('rest1=',rest1)
    l2=rest1.find('=') +1
    r2=rest1.find('|')
    statu=rest1[l2:r2]
    #print(statu)
    
    rest2=rest1[r2+1:]
    #print(rest2)
    l3=rest2.find('=') + 1
    end_time=rest2[l3:]
    #print(start_time)
    #print(statu)
    data={}
    data['start_time']=start_time
    data['statu']=statu
    data['end_time']=end_time
    #print(end_time)
    return data


# In[16]:


def check_Masturbation(data):
    
    print('=========戒冲小助手=========')
    print('请随意分享该程序')
    print()
    start_time = int(data['start_time'])
    true_time = (int(time.time()))
    past_time = true_time - start_time
    past_days = int(past_time/86400)
    print('距离上次打卡已经',past_time,'秒，即',past_days,'天')
    Masturbation = data['statu']
    if Masturbation == 'progressing':
        if int(past_days) > 1:
            print('哇，好棒哦！你已经坚持了',past_days,'天')
        if int(past_days) < 15:
            title='初心贤者称号\n\t坚持满15天可以解锁下一个称号哦！'
        elif 15<= int(past_days) < 30:
            title='小成贤者称号\n\t坚持满30天可以解锁下一个称号哦！'
        elif 30<= int(past_days) < 60:
            title='大成贤者称号，坚持满60天可以解锁下一个称号哦！'
        elif 60<= int(past_days) <100:
            title='封圣贤者称号\n\t坚持满100天可以解锁下一个称号哦！'
        elif 100 <= int(past_days):
            title='阳光男孩称号\n\t不过你可能患上了阳痿，请注意身体，去医院好好检查哦！'
            
        print('恭喜你获得',title)
    else:
        start_time = int(data['start_time'])
        end_time = int(data['end_time'])
        past_time = end_time - start_time
        past_days = int(past_time/86400)
        print('你早就失败了，你只坚持了',past_time,'秒，即',past_days,'天')
        return 'fail'
    Masturbation = input('\n \n今天你冲了吗？\n\t冲了请输入y，没冲输入n： ').upper()
    
    if Masturbation == 'Y':
        print('\t你冲了，你失败了')
        print()
        data = 'start_time=' + str(start_time) + "|statu=fail" + "|end_time=" + str(true_time)
        
        record = 'Record'
        file = open(record,'w')
        file.write(data)
        file.close
    else:
        input('\t居然没冲，很棒，再接再厉哦！')
        return 'progressing'


# In[20]:


if __name__ == '__main__':
    
    data = read_record()
    statu = check_Masturbation(data)
    if statu == 'fail':
        if input('\t重置记录？ y/n') == 'y':
            record = 'Record'
            file = open(record,'w')
            data = 'start_time=' + str(int(time.time())) + "|statu=progressing" + "|end_time="
            file.write(data)
            file.close
            file = open(record,'r')
            print('\t记录已重置')
        else:
            print('\t记录维持原样')

