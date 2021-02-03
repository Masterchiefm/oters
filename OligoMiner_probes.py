#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import dna_tools

def convert():
    file_name = input('输入源文件csv路径')
    output_name = input('输入保存的文件名') + '.fasta'

    primers=''
    primers=''
    data = {'name':"", 'start':'' , 'stop':''}
    all_data=[]
    count = 1
    with open(file_name,'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if 'sequence' in row:
                pass
            else:
                data['name'] = row[0]
                data['start'] = row[1]
                data['stop']=row[2]
                data['sequence'] = row[3]
                data['Tm'] = row[5]
                #print (data['Tm'] )
                #print(dna_tools.tm(data['sequence']))
                #print('------------------------------')
                all_data.append(data)
                primers = primers + '>' + data['name'] + '_probe_' + str(count) + '\n' + data['sequence'] + '\n\n'
                count = count + 1
                
                
    result = open(output_name,'w')
    result.write(primers)
    result.close
    print('done\n')


# In[2]:


if "__main__" in __name__:
    while True:
        convert()
            
            
            
        
            


# In[14]:





# In[ ]:




