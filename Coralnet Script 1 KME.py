#!/usr/bin/env python
# coding: utf-8

# This is the first of three scripts used to run Coralnet. 
# This script goes through each of the photos and makes a JSON file which we then feed to CN along with the photos themselves as an instruction manual so to speak. 

# Import your libraries

# In[ ]:


import pandas as pd
import numpy as np
import requests 
import time
import os


# Tell it how to log into CN online

# In[ ]:


url= 'https://coralnet.ucsd.edu/api/token_auth/' 
payload= '{"username": "YOURUSERNAMEHERE", "password": "YOURPASSWORDHERE"}'
headers={"Content-type": "application/vnd.api+json"}
coralnet_token=requests.post(url, data=payload, headers=headers).text.split(':"')[-1][:-2]
print(coralnet_token) #just a check to make sure you got a token


# In[ ]:


import dropbox
import json
import random
import time 
from PIL import Image


#This portion defines variables
#You will want to break your images into batches in case the script fails midway due to internet issues, to prevent loss. 
#Just turn on (uncomment) one at a time. 
#In Py comments are preceded by hashtag. 


#The first variable is the folder you want to search for on Dropbox and will also be how the resulting JSON will be named
#This is relative to the dropbox path, so wherever you find your Dropbox app folder, leave out that first part of the path
#and just tell it which subfolder to use. 
#for example, my app is here: #dropbox_path = '/Apps/CoralnetAppRedSea' so these are folders within that path.

#folder_to_use = '/PQ1' 
#folder_to_use = '/PQ2' 
#folder_to_use = '/PQ3' 
#folder_to_use = '/PQ4' 
#folder_to_use = '/PQ5' 
#folder_to_use = '/PQ6' 
#folder_to_use = '/PQ7' 
#folder_to_use = '/PQ8' 
#folder_to_use = '/PQ9' 
#folder_to_use = '/PQ10' 
folder_to_use = '/PQ11' 


local_path = 'C:\\Users\\BLAH\\Desktop\\BLAH\\' #Replace BLAH with wherever you want to keep your output files locally.
#This is the pathway on you local machine where these files will be saved and located. Keep the double slashes.

dropbox_token = 'MYSUPERLONGTOKEN' 
#Replace this with the authorization token for your Dropbox app.

#Connects to our Dropbox account
dbx = dropbox.Dropbox(dropbox_token)
dbx.users_get_current_account()

#Creates empty list to store the file names within the folder of interest
file_list = []

#Pulls out first files from the folder, adds the names to file_list, then creates a cursor 
#signifying its end location in the folder
file_list_all = dbx.files_list_folder(f'{folder_to_use}')
file_list.extend(file_list_all.entries)
file_cursor = file_list_all.cursor

keep_retrieving = True #Sets this as True, and will change to False when all files retrieved
while keep_retrieving: #Loops through to retrieve the rest of the images
    file_list_continue = dbx.files_list_folder_continue(file_cursor)
    file_list.extend(file_list_continue.entries)
    file_cursor = file_list_continue.cursor
    
    if len(file_list_continue.entries) == 0:
        keep_retrieving = False

dat = {"data":[]}

#This block can be uncommented to generate the list of file names from Dropbox
#Can be used to check which images didn't upload in the case of errors during the upload process
file_dict = {}
k = 1
for entry in file_list:
    file_dict[f'row_{k}'] = entry.name
    k += 1
    
import pandas as pd
file_list = pd.DataFrame.from_dict(file_dict, orient = 'index')
file_list.to_csv(f'{local_path}{folder_to_use}_file_list.csv', index=False)

listoflist=pd.read_csv(f'{local_path}{folder_to_use}_file_list.csv', index_col=0)
for row in listoflist.iterrows(): 
#iterrows documentation: https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
#   print(row[0])
    pathway = f'{folder_to_use}/' + row[0]
    tmp_name = dbx.sharing_create_shared_link(path = pathway, short_url=False, pending_upload=None)
    #time.sleep(30) #you can sleep it if you like; if it's kicking you off.

    
#THE FOLLOWING PORTION IS DEPENDENT ON PIXEL SIZE FOR EACH IMAGE AND NEEDS TO BE CHANGED FOR DIFFERENT IMAGE SIZES.
#Most our JPG files are x=5472* y=3648 pixels
#or they are x=3648 y=5472 pixels, but it doesn't matter because we can rotate them first
#instructions for that in 'coralnet batch renaming and pooling' script
#We have a 5% buffer on the outside of the image
# 0.05* 5472 = 273.6
#0.05*3648 = 182.4
#making the boundary from 274 to 5198 x axis (picking closest whole number pixel)
#and from 182 to 3466 on the y axis
    
#Option later to insert a check for the dimensions of the image
#or pick random integer within 95% of the width; 95% of the length of the image

#Option later to change this to stratified random selection (not done yet; these are random points)

#OR I can sort the images first, put them in different folders and then annotate ?

#the following works for the  x=5472* y=3648 pixel files. 
#ROWS refer to the Y AXIS and COLUMNS in this script refer to the X-AXIS.
    patience=60
    to_append = {"type": "image", 
                "attributes":{"url":tmp_name.url[:-1] + '1', 
                              "points":[
                                      {"row": random.randint(182, 3466), 
                                      "column": random.randint (274, 5198)}, 
                                      {"row": random.randint(182, 3466), 
                                      "column": random.randint (274, 5198)},
                                      {"row": random.randint(182, 3466), 
                                      "column": random.randint (274, 5198)},
                                      {"row": random.randint(182, 3466), 
                                      "column": random.randint (274, 5198)},
                                      {"row": random.randint(182, 3466), 
                                      "column": random.randint (274, 5198)},
                                      {"row": random.randint(182, 3466), 
                                      "column": random.randint (274, 5198)},
                                      {"row": random.randint(182, 3466), 
                                      "column": random.randint (274, 5198)},
                                      {"row": random.randint(182, 3466), 
                                      "column": random.randint (274, 5198)},
                                      {"row": random.randint(182, 3466), 
                                      "column": random.randint (274, 5198)},
                                      {"row": random.randint(182, 3466), 
                                      "column": random.randint (274, 5198)},
                                      
                                      ]
                                  }
                              }
    dat['data'].append(to_append)
#10 points -- option to add more.
#Option to replace with points sampled by the CN user (to test accuracy of robot vs human more specifically)

with open(f'{local_path}{folder_to_use}.json', 'w') as outfile:
    json.dump(dat, outfile)

