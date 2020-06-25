#!/usr/bin/env python
# coding: utf-8

# In[9]:


# 用以生成wav文件
import wave
import math
import struct

name='歌唱动荡的青春'
print('生成音频：',name)
file=wave.open(name + ".wav","w")
file.setframerate(8000)
file.setnchannels(1)
file.setsampwidth(2)


def wv(code=[262,1],v=1,wf=file,sr=8000):
    '''
    t:写入时长
    f:声音频率
    v：音量
    wf：一个可以写入的音频文件
    sr：采样率
    '''
    f = float(code[0])
    t = float(code[1])
    
    tt=0
    dt=(1.0/sr)*2 #一个四拍子
    while tt<=t:
        
        #算出波形的值，然后逐个写入文件中
        s=math.sin(tt*math.pi*2*f)*0.5*32768#输出的是声音的波形，v调节音量，映射到[-2^15,2^15)
        #s = 13833
        s=int(s)
        
        fd=struct.pack("h",s)#转换成8bit二进制数据
        wf.writeframes(fd)#写入音频文件
        tt+=dt#时间流逝
def decode(code):
    '''
    更方便输入音符，输入的是字符，或者数字。
    输入'1_2'即为音符1，2拍。如果只输入1这样的，默认一拍。H为分拍子的符号
    '''
    scal = {'0.1': 131.0, '0.2': 147.0, '0.3': 165.0, '0.4': 174.5, '0.5': 196.0, '0.6': 220.0, '0.7': 247.0,'1.0':262,'2.0':294,"3.0":330,"4.0":349,"5.0":392,"6.0":440,"7.0":494,'10.0': 524, '20.0': 588, '30.0': 660, '40.0': 698, '50.0': 784, '60.0': 880, '70.0': 988,"0.0":0}
    if code == 'H':
        return 0
    code = str(code)
    #print(code)
    l = code.find('_')
    #print('l',l)
    if l == -1 :
        #print(code)
        i = float(code)
        t = 1 
    else:
        #print(code[:l])
        i = float(code[:l])
        t = float(code[l+1:])
    
    print('音符',i,'节拍',t)
    
    return [scal[str(i)],t]
    
def music(song = [1,2,3,4,5,6,7]):
    for i in song:
        code = decode(i)
        #print(code)
        if code:
            wv(code)
            #input('c')
        else:
            pass   


# In[10]:


H = 'H'
p1 = [0.3,H,0.6,'0.6_0.75','0.7_0.5',1,0.6,H,4,'3_2',1,H,2,2,3,'2_0.75','1_0.25',H,0.7,'0.6_2']
p2 = [0.3,H,0.6,'0.6_0.75','0.7_0.25',1,0.6,H,6,'5_2',3,H,4,'4_0.75','3_0.5',4,5,H,'3_2']
p3 = [3,H,'6_2','10_2',H,7,'6_2','5_0.5','6_0.5',H,'7_1.5','6_0.5',5,6,H,'3_2']
p4 = [1,H,'6_2','5_1.5','4_0.5',H,3,'2_2',4,H,3,'2_0.5','3_0.5',4,3,H,'6_3',0]

music(p1 + p2 + p3 + p4)
file.close
import os
input('播放？')
print('开始播放')
os.system('cvlc '+name +'.wav')


# In[ ]:




