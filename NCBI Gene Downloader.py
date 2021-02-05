#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# url = https://www.ncbi.nlm.nih.gov/nuccore/NC_000019.9?from=41330323&to=41353922&report=fasta&strand=true


# In[ ]:


from re import search,sub
from requests import get


# In[17]:


def banner():
    print('============================================================== ')
    print('                       NCBI Gene Downloader                    ')
    print('                                                               ')
    print('                            By Qiqin Mo                        ')
    print('============================================================== ')
    print('Description:                                                              ')
    print('    Input gene location, the script will output genebank file ')
    print('Usage:                                                         ')
    print('    Search gene name in NCBI Gene data base, then copy the     ')
    print('    location in Genomic context volume. \n                       ')
    print('    For example:                                               ')
    print('      1. I copied "NC_000019.9 (41836228..41859827, complement)" ')
    print('      2. paste it on the "location" prompt line. ')
    print('      3. If I want to expand the selected gene range, I will type the base number then.')
    print('      4. Waite a second, the .gb file will be saved.')
    print('===============================================================')
    


# In[ ]:


def get_genebank():
    
    location = input('location: example: NC_000019.9 (41836228..41859827, complement) \n')
    
    locus = search('NC_0+[0-9]+\.[0-9]+',location).group()
    start = search('\([0-9]+\.',location).group().replace('(','').replace('.','')
    stop = search('\.\.[0-9]+',location).group()
    #print(stop)
    stop = search('[0-9]+',stop).group()
    complement = search ('complement',location)
    
    if complement:
        strand = "&strand=true"
    else:
        strand = ''
        
        
    add = input ('add more bases from upstream： ').replace(' ','')
    if add == '':
        add = 0
    add2 = input('add more bases from dowmstream:  ').replace(' ','')
    if add2 == '':
        add2 = 0
    if add:
        if strand:
            stop = str(int(stop) + int(add))
            start = str(int(start) - int(add2))
        else:
            start = str(int(start) - int(add))
            stop = str(int(stop) + int(add2))
        
        

    
    url = "https://www.ncbi.nlm.nih.gov/nuccore/" + locus + "?from=" + start + "&to=" + stop + "&report=genebank" + strand
    print('You can browse the following url:\n' + url + '\n')
    input('Press Enter to continue downloading...')
    print('downtloading...')
    page_uid = get(url)
    uid = search('ncbi_uid=[0-9]+',page_uid.content.decode('utf-8')).group().replace('ncbi_uid=','')
    genebank_url = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id="+ uid + "&db=nuccore&report=genbank&&from=" + start + "&to=" + stop + "&retmode=html&withmarkup=on&tool=portal&log$=seqview&maxdownloadsize=1000000"
    return genebank_url
    
    
    
    


# In[ ]:


def main():

    name = input('\nInput the gene as:\n') + '.gb'
    url = get_genebank()
    
   # print(url)
    page = get(url).content.decode('utf-8')
    result = search('<pre(.|\n)*/pre>',page).group()
    gb = sub('<script.*/script>','',result)
    gb = sub('<.*?>','',gb)
    
  
    with open(name, 'w') as my_open:
        my_open.write(gb)
        my_open.write('\n')
        my_open.close
    print('GeneBank file saved as ' + name)
    #input('')
    


# In[ ]:


banner()
while True:
    main()


# In[18]:


banner()


# In[ ]:




