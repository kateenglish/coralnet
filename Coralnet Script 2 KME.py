#!/usr/bin/env python
# coding: utf-8

# The previous script makes the JSON file instructions for CN for each image. 
# This script feeds the JSON and the images to CN via Dropbox. 
# This would be the script to amend if we wanted to use OneDrive or some other online file folder. 

# First, initiate functions.

# In[ ]:


import json
import numpy as np
import pandas as pd

def get_points(height, width, h_offset, w_offset, percentage, sampling_method):
    '''
    height: the height of the image (rows)
    width: the width of the image (columns)
    offset: the % of pixels on all sides to avoid sampling (i.e. avoids edges of image)
    percentage: the % of points to sample (1% of a 4MP image = 40,000 points)
    sampling_method: either "random" or "grid"
    '''

    percentage = percentage * .01

    num_points = int(height * width * percentage)

    if(sampling_method == 'random'):

        x = np.random.randint(w_offset, width - w_offset, num_points)
        y = np.random.randint(h_offset, height - h_offset, num_points)
        
    else:
        
        density = int(np.sqrt(num_points)) 

        # Creates an equally spaced grid, reshapes, converts into list
        x_, y_ = np.meshgrid(np.linspace(w_offset, width - w_offset, density), 
                             np.linspace(h_offset, height - h_offset, density))

        xy = np.dstack([x_, y_]).reshape(-1, 2).astype(int)

        x = [point[0] for point in xy]
        y = [point[1] for point in xy]

        # Any labels that did not fit in the grid will be sampled randomly
        x += np.random.randint(w_offset, width - w_offset, num_points - len(xy)).tolist()
        y += np.random.randint(h_offset, height - h_offset, num_points - len(xy)).tolist()


    points = []

    for _ in range(num_points):
        points.append({'row': int(y[_]), 'column': int(x[_])})
        
    return points


def decode_status(r_status):
    
    curr_status = json.loads(r_status.content) 
    message = ''
    
    if 'status' in curr_status['data'][0]['attributes'].keys(): 
    
        s = curr_status['data'][0]['attributes']['successes'] 
        f = curr_status['data'][0]['attributes']['failures'] 
        t = curr_status['data'][0]['attributes']['total']
        status = curr_status['data'][0]['attributes']['status'] 
        ids = curr_status['data'][0]['id'].split(",")
        ids = ''.join(str(_) for _ in ids)

        message = 'Success: ' + str(s) + ' Failures: ' + str(f) + ' Total: ' + str(t) + ' Status: ' + str(status) + ' Ids: ' + ids
    
    return curr_status, message


def check_status(r):
    
    # Sends a request to retrieve the completed annotations, obtains status update
    r_status = requests.get(url = 'https://coralnet.ucsd.edu' + r.headers['Location'], 
                            headers = {"Authorization": f"Token {coralnet_token}"})

    # Extracts the content from the status update
    curr_status, message = decode_status(r_status)
        
    return curr_status, message    

def convert_to_csv3(export):
    
    all_preds = pd.DataFrame()
    
    for i in range(len(export['data'])): #This number MUST MATCH the batch size. 

        image_file = export['data'][i]['id'].split("/")[-1].split("?")[0]

        for point in export['data'][i]['attributes']['points']:

            per_point = dict()

            per_point['image'] = image_file

            per_point['X'] = point['column']
            per_point['Y'] = point['row']

            for index, classification in enumerate(point['classifications']):

                per_point['score_' + str(index + 1)] = classification['score']
                per_point['label_id_' + str(index + 1)] = classification['label_id']
                per_point['label_code_' + str(index + 1)] = classification['label_code']
                per_point['label_name_' + str(index + 1)] = classification['label_name']

            all_preds = pd.concat([all_preds, pd.DataFrame.from_dict([per_point])])
    
    return all_preds


# Then run the images through.

# In[ ]:


#change this to the local location of your json file that you made in your last script. 
#I like to keep mine in a desktop folder.
#If you made multiple you can iterate or run file by file. 
#I actually do the latter because internet bandwidth necessitates babysitting.

with open('C:\\LOCALLOCATIONOFMYJSONFILE.json', 'r') as file: 
  data3 = json.load(file)

# How long to wait before asking for another status update
patience = 60
classifier_url = 'https://coralnet.ucsd.edu/api/classifier/CURRENTROBOTNUMBER/deploy/' #Change this to the current robot
import dropbox
import json
import random
import time 
from PIL import Image
import glob

#Give it a glob file of all your images
#change this to have the correct paths.
img_files = glob.glob('C:\\Users\\YOURUSERNAME\\Dropbox\\Apps\\YOURDROPBOXAPPNAME\\YOURDBAPPSUBFOLDERNAME\\*.jpg') 

#Defines variables
#change this to your app subfolder name
folder_to_use = '/APPSUBFOLDERNAME' 

######

#This variable is the folder you want to search for on Dropbox and will also be how the resulting JSON will be named
#change to the proper folder you like your output stored in.
output_folder = 'C:\\Users\\YOURUSERNAME\\Desktop\\THEFOLDERYOUKEEPYOUROUTPUTIN\\' 

#Saves the classifier URL you will be using and your CoralNet authorization token
headers = {"Authorization": f"Token {coralnet_token}", #you called this token in the last script.
           "Content-type": "application/vnd.api+json"}
# Looping through each file

####Initiating variables for the loop.
k=0
dat_length=100

while dat_length==100:
    dat=data3['data'][k:k+100]
    dat_length=len(dat)
    if dat_length==0:
        break
    # For feedback purposes
    reported = False
    
    # Break the data into batches of N (CoralNet requirement). 100 is the greatest number available for CN.
    current_batch = {"data" : data3['data'][k : k + 100]} 
    
    # Creates an individual request from our JSON request file
    with open(f'{output_folder}Batch_{str(k+100)}.json', 'w') as outfile:
        json.dump(current_batch, outfile)
    
    print("\nCurrently on batch:", str(k + 100), " containing:", len(current_batch['data']), " entries.")

    # Sends the requests to the `source` and in exchange we recieve a message telling us if it was recieved correctly.
    r = requests.post(url = classifier_url, data = open(f"{output_folder}Batch_{str(k+100)}.json"), headers = headers) 
    
    # If request didn't go through, end the loop and change the settings according to the error
    if(r.content.decode() != ''):
        print("Error: ", r, r.content)
        break
    else:
        print("Request sent successfully! Please wait", patience, "seconds")

    # Waits N seconds before attempting to retrieve results
    time.sleep(patience)     
    in_progress = True
    
    # Pings CoralNet every N seconds to check the status of the job
    while in_progress:
        
        # Get an update on our request
        curr_status, message = check_status(r)
        
        # Not complete yet, wait N seconds and then ask again
        if message != '': 
            if(reported):
                print('.')
            else:
                print(message)
            reported = True
            time.sleep(patience) 
        
        # It's complete! Store the annotations in export, close while loop, goes to the next image.
        else: 
            print("Finished ", str(k + 100), " batch" )
            
            predictions = convert_to_csv3(curr_status) #changed to my script, convert_to_csv3, to handle multiple entries
            predictions.to_csv(f'{output_folder}Batch_{str(k+100)}.csv')
            
            #export['data'].extend(curr_status['data'])
            
            in_progress = False
    k+=100 #reassigning _ for the next loop 


# Give it plenty of time to run. It should print ellipses while running.
# What to do if it stops?
# First export the curr_status and edit.

# In[ ]:


#uncomment this if you want to print the partial outputs of a failed or stalled run.
#change the folder paths in caps. 

#predfail=convert_to_csv3(curr_status)
#predfail.to_csv('C:\\Users\\Desktop\\LOCALFILEPATHNAMEDWHATEVERYOULIKE.csv')

#with open('C:\\Users\\YOURUSERNAME\\Desktop\\THEPLACEYOUKEEPYOURJSONSCRIPT.json', 'r') as file:
#  data1 = json.load(file)
#predfail=convert_to_csv3(data1)
#predfail.to_csv('C:\\YOURCHOSENPATHANDNAME.csv')

