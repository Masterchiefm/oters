#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from reportlab.platypus import SimpleDocTemplate,Image, PageBreak
from reportlab.lib.pagesizes import A4, landscape
import time
from PIL import Image as pilImage


# In[ ]:



def findbooks(dirPath):
    if dirPath:
        pass
    else:
        dirPath = '.'
    #【文件夹路径, 文件夹名字, 文件名】
    books = []
    for root,docname, filename in os.walk(dirPath):
        book = {"root": "", "pages": ''}
        #print('ane=',filename)
        if  'jpg' in str(filename):
            #print('有图')
            book['root']=root
            book['pages']=len(filename) - 1
            books.append(book)
            #print(books)
    return books


# In[ ]:





# In[ ]:


def makepdf(book):
    
    root = book['root']
    pages = book['pages']
    # A4 纸的宽高
    __a4_w, __a4_h = landscape(A4)
    #print(landscape(A4))
    bookDoc = SimpleDocTemplate(root+'''.pdf''', pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    i = 1
    bookPagesData=[]
    while i < pages :
        page = root + (os.sep) + str(i) + ".jpg"
        #print(page)
        try:
            img_w, img_h = ImageTools().getImageSize(page)
            # img_w = img.imageWidth
            # img_h = img.imageHeight
        except:
            i = i + 1
            continue
            
        if __a4_w / img_w < __a4_h / img_h:
            ratio = __a4_w / img_w
        else:
            ratio = __a4_h / img_h
        data = Image(page, img_w * ratio, img_h * ratio)
        #data = Image(page)
        bookPagesData.append(data)
        bookPagesData.append(PageBreak())
        i = i + 1
    try:
        #print(bookDoc)
        bookDoc.build(bookPagesData)
        
    except Exception as err:
        print("[*][转换PDF] : 错误. [名称] > [%s]" % (root))
        print("[*] Exception >>>> ", err)
    


# In[ ]:


class ImageTools:
    def getImageSize(self, imagePath):
        img = pilImage.open(imagePath)
        return img.size


# In[ ]:


books = findbooks('.')
for book in books:
    print(book)
    makepdf(book)
    print('转换完成')

