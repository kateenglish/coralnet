#!/usr/bin/env python
# coding: utf-8

# In[5]:


#Import directories
import pandas as pd
import numpy as np
import shutil
import sys
import os


# This script is to rename each image in a directory based on its parent folders (A) and move those images to a single folder so they can be fed to coralnet (B). 

# First, name each of your folders. 
# Replace the directories below with your own file paths.

# In[17]:


dir1='C:\\Users\\user\\Desktop\\PQ1'
dir2='C:\\Users\\user\\Desktop\\PQ2'
dir3='C:\\Users\\user\\Desktop\\PQ3'
dir4='C:\\Users\\user\\Desktop\\PQ4'


# SCRIPT A: This script renames 

# In[21]:


#Replace the name of your directory here and walk through each of your directories.

#for root, dirs, files in os.walk(dir1):
#for root, dirs, files in os.walk(dir2):
#for root, dirs, files in os.walk(dir3):
for root, dirs, files in os.walk(dir4):
    #print(files) #this gives either an empty set or a set of n files with extension .docx
    #print(len(files))
    for i in files:
        if len(files)>0:
            #print(i) #this actually gives each file name without the file extension and without any blanks.
            print(root+"\\"+i)  #this successfully prints all of the file paths of all the files. 
            oldpath=root+"\\"+i 
            
            newname=(root.replace('\\', '_')[26:]+'_'+i)
            #print(newname)
            #print(oldpath+"\\"+newname)
            newpath=root+"\\"+newname
            print(newpath)
            os.rename(oldpath, newpath)
        else:
            continue
#If you would like to list all files in your directory just to see what exists, use this:
#for files in os.walk(dir):
#    print(files)
    #for i in range(len(files)):
    #    print(files[i])


# In[15]:


#Need to remove anything with the name 'SITE' in it from the pool.


# SCRIPT B: This script moves to a single folder.

# In[32]:


#Replace the name of your directory here and walk through for each of your directories: 

import shutil
for root, dirs, files in os.walk(dir1):
#for root, dirs, files in os.walk(dir2):
#for root, dirs, files in os.walk(dir3):
#for root, dirs, files in os.walk(dir4):
    #print(files) #this gives either an empty set or a set of n files with extension .docx
    #print(len(files))
    for i in files:
        #if 'SITE' in i:
        #    print('nope')
        if 'SITE' not in i:    
            if len(files)>0:
                #print(i) #this actually gives each file name without the file extension and without any blanks.
                print(root+"\\"+i)  #this successfully prints all of the file paths of all the files. 
                oldpath=root+"\\"+i 
            
                newroot=r'C:\Users\user\Desktop\PQ1Pool'
                #newroot=r'C:\Users\user\Desktop\PQ2Pool'
                #newroot=r'C:\Users\user\Desktop\PQ3Pool'
                #newroot=r'C:\Users\user\Desktop\PQ4Pool'
                newhome=newroot+"\\"+i
                print(newhome)
                shutil.move(oldpath, newhome)
            else:
                continue


# Note this is not perfect because we still have _Store files that need to be manually deleted. 
# Also, ideally we'd be copying the files rather than moving them, but moving them saves space on my computer so for now I'll keep it like this. 
# There are also some files that have unsupported file formats, though they say JPG :/
# May want to rewrite this to include 'site' and 'Site' as well as 'SITE' because I did find some stragglers.

# # To Rotate Images Simply Add 'Dimensions' to the search field under View>Details by right clicking the banner, then click Dimensions, select and rotate! 

# In[ ]:




