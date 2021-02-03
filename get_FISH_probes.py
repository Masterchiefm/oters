#!/usr/bin/env python
# coding: utf-8

# In[1]:

print('----------------------------------')
print('--------FISH Probes Finder--------')
print('--------                  --------')
print('--------         M        --------')
print('----------------------------------')
import dna_tools
import csv


# In[2]:

#data = {'probename':'','chr':line[0], 'start':int(line[1] ), 'end':int(line[2]), 'sequence':line[3] ,'gc':line[4]}
def openfile(file_path):
    f = open(file_path)
    list = []
    for line in f.readlines():
        try:
            line = line.split()
            data = {'probename':'','chr':line[0], 'start':int(line[1] ), 'end':int(line[2]), 'sequence':line[3] ,'gc':line[4]}
            list.append(data)
        except:
            print('unknow error')
    f.close()
    
    
    return list
        


# In[3]:


#输入起始位点 38115134
#输入结束位点 38115629
#hg19_chr9b.bed


# In[4]:
def search():
    database = input('输入/拖拽要读取的数据库路径：\n' )
    start = int(input('输入起始位点\n '))
    end = int(input('输入结束位点\n '))
    output_file=input('输入结果保存文件名：\n ')
    probename = input('输入保存的探针名:\n')
    f = openfile(database)
    
    
    outputs =[]
    output_probes = ''
    last = 0
    count = 1
    for data in f:
        #print(data['start'], start)
        
        if int(data['start'] > start) and (data['end'] < end):
            
            tm = dna_tools.tm(data['sequence'])
            data['tm'] = tm
            distance = data['start']-last
            last = data['end']
            
            marker = ''
            if distance < 10:
                data['distance'] = "Distant is too short! It's" + str(distance)
            else:
                data['distance'] = distance
                
            data['note'] = ''    
            if 'AAAAA' in data['sequence'] or 'TTTTT' in data['sequence']:
                data['note'] = data['note'] + '5 x A/T'
                marker = marker + 'A*'
            if 'GGGG' in data['sequence'] or 'CCCC' in data['sequence']:
                data['note'] = data['note'] + '4 x C/G'
                marker = marker + 'G*'
            
            probe = probename + "_" + str(count) + marker
            data['probename'] = probe
            outputs.append(data)
            output_probes =  output_probes + ">" + probe + '\n' + data['sequence'] + '\n'
            count = count + 1
            #print(data)
        else:
            #print('无')
            pass
    


# In[6]:


    headers = ['name','chr', 'start','end','sequence','GC','TM','distance','note']
    rows = []
    for data in outputs:
        row = [data['probename'],data['chr'],data['start'],data['end'],data['sequence'],data['gc'],data['tm'],data['distance'],data['note']]
        rows.append(row)
    

    
    with open(output_file+".csv",'w',newline='')as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)
        
    with open(output_file + ".fasta", 'a') as fasta:
        fasta.write(output_probes)
        fasta.close()
        
    print('Done! results in ',output_file)
   





# In[5]:

if __name__ == '__main__':
    
    while True:
        search()
        input('按回车继续？或者直接关闭程序\n')
    
