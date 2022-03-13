#!/usr/bin/env python
# coding: utf-8

# You have output in the form of csv files stored in your local path as directed.
# Here's how to put them together into a single file that's human-readable.
# 
# This is sloppy scripting--feel free to give it a way to iterate through all files by glob if you like. 
# I generally have many batches worth of data to combine. 

# In[ ]:


import glob
csv_files1 = glob.glob('C:\\Users\\YOURUSERNAME\\Desktop\\YOURLOCALFILEOUTPUT\\*.csv')
#If you have multiple folders of data you can name them here e.g. 'csv_files2...etc'


# In[ ]:


run1_data = pd.DataFrame()
list_ = []
for file_ in csv_files1:
    df = pd.read_csv(file_,index_col=None,)
    list_.append(df)
    run1_data = pd.concat(list_)
    print(file_ + " has been imported.")


# In[ ]:


#check that it's the anticipated size
run1_data.shape


# In[ ]:


#if you have multiple folders of data you can do something like this.
#finalconcat=pd.concat([run1_data, run2_data, run3_data, run4_data, run5_data, run6_data, run7_data, run8_data, run9_data, run10_data, run11_data, run12_data, run13_data, run14_data], axis=0)


# In[ ]:


#check that the output is the anticipated size
finalconcat.shape


# In[ ]:


finalconcat.to_csv('C:\\Users\\YOURUSERNAME\\Desktop\\YOURLOCALOUTPUTPATH.csv')

