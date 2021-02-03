#!/usr/bin/env python
# coding: utf-8

# In[71]:


def tm(sequence):
    
    sequence = str(sequence).strip().lower().replace(' ','').replace('u','t')
    import primer3
    #from primer3 import calcTm
    tm = int(primer3.calcTm(sequence))
    
    if float(tm) < 0:
        print('请检测序列是否输入正确')
        return 0
    #print ('Tm is',tm,'℃')
    
    #返回 str
    return int(tm)


# In[18]:


def reverse_dna(sequence):
    
    #sequence = sequence.lower().replace(' ','')
    print('5->3 original sequence: \n')
    print('5-',sequence,'-3')
    reverse = ''
    for code in sequence:
        if code == "a":
            reverse = reverse + 't'
        elif code == "t":
            reverse = reverse + 'a'
        elif code == "c":
            reverse = reverse + 'g'
        elif code == "g":
            reverse = reverse + 'c'
        else:
            print('错误碱基')
            reverse.append('#')
    

    print('3-',reverse,'-5')
    new_sequence = reverse[::-1]
    
    #返回互补序列，5->3
    return new_sequence






