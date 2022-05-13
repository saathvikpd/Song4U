from sre_constants import SUCCESS
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import time
import matplotlib.pyplot as plt
import numpy as np

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.layers.experimental.preprocessing import Rescaling

import pathlib
import pandas as pd
import glob
import os
import random
import sys
import requests

import webbrowser
import requests
import json
import csv
import random
import os
from tkinter import *
from PIL import Image, ImageTk
import time

# =============================================================================
# import os, sys
# my_lib_path = os.path.abspath('/Users/saathvikdirisala/Downloads/Python/API/')
# sys.path.append(my_lib_path)
# =============================================================================

from Overall import addsongs

#clientID = 'e46921ad8e01410abc08418d259f27a2'
#clientSECRET = 'e20db8a2685342de9047477a47d94aa9'

#webbrowser.open("https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&scope=playlist-modify-private&redirect_uri=https://github.com/mohakvni/Song4U".format(CLIENT_ID = clientID))

# =============================================================================
# def addsongs(threshold):
#     
# 
#     threshold = threshold//10
#     threshold_sad = 10 - threshold
#     webbrowser.open("https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&scope=playlist-modify-private&redirect_uri=https://github.com/mohakvni/Song4U".format(CLIENT_ID = clientID))
# 
#     
#     retrieve_input()
#     
#         
#     f = open("/Users/saathvikdirisala/Downloads/Python/API/temp.txt", "r")
#     redirect = f.read()
#     #print([redirect])
#     f.close()
#     
#     redirect = input("enter an arg")
#     temp = redirect.split("=")
#     code_  = temp[1]
# 
#     AUTH_URL = 'https://accounts.spotify.com/api/token'
# 
#     # POST
#     auth_response = requests.post(AUTH_URL, {
#         'grant_type': 'authorization_code',
#         'client_id': clientID,
#         'client_secret': clientSECRET, 
#         'code' : code_,
#         'redirect_uri' : 'https://github.com/mohakvni/Song4U'
#     })
# 
#     # convert the response to JSON
#     auth_response_data = auth_response.json()
# 
# 
#     access_token = auth_response_data['access_token']
# 
# 
#     def get_UserID(code_):
# 
#         response = requests.get("https://api.spotify.com/v1/me", headers = {
#             "Content-Type":"application/json","Authorization": "Bearer {token}".format(token=access_token)})
# 
#         content = response.json()
#         return content["id"]
# 
# 
#     headers = {"Content-Type":"application/json",
#         'Authorization': 'Bearer {token}'.format(token=access_token)
#     }
# 
#     os.chdir("API")
# 
#     f_happy= open ("./happy.csv","r")
#     f_sad = open("./sad.csv","r")
#     row_happy = csv.reader(f_happy)
#     row_sad = csv.reader(f_sad)
# 
#     happy_list = []
#     for i in row_happy:
#       happy_list.append(i[1])
# 
#     sad_list = []
#     for i in row_sad:
#         sad_list.append(i[1])
# 
#     temp = random.randint(1,1000)
#     hlist = happy_list[temp-threshold:temp]
#     slist = sad_list[temp-threshold_sad:temp]
#     overall = hlist + slist
# 
# 
#     user_id = get_UserID(code_)
# 
#     endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
#     request_body = json.dumps({
#               "name": "Mood",
#               "description": "We created a playlist depending on if we think you are happy or sad",
#               "public": False
#             })
#     response = requests.post(url = endpoint_url, data = request_body, headers= headers)
#     playlist_id = response.json()['id']
#     endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
# 
#     request_body = json.dumps({
#               "uris" : overall
#             })
#     response = requests.post(url = endpoint_url, data = request_body, headers= headers)
#     if response.status_code == 201:
#         print("We gotchya")
#     else:
#         print("Oops, there seems to be an error")
# =============================================================================


def LoadModel():
    tf.keras.backend.clear_session()

    model_dir_1 = "/Users/saathvikdirisala/Downloads/Python/Model60.h5"

    mirrored_strategy = tf.distribute.MirroredStrategy()
    with mirrored_strategy.scope():
        model_1 = load_model(model_dir_1)
    return model_1
        
def openCamera(model_1):
    classes = ["Happy", "Neither", "Sad"]

    cap = cv2.VideoCapture(0)


    t = 0
    ensemble = []
    while t<150:
        t+=1
        success, img = cap.read()
    # imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        #print(type(img), img.shape)
        if t%5==0:
            test_data = cv2.resize(img, (224, 224))
            test_data = cv2.cvtColor(test_data, cv2.COLOR_RGB2GRAY)
            test_data = cv2.cvtColor(test_data, cv2.COLOR_BGR2RGB)
            test_data = test_data/255.
            test_data = np.array([test_data])
            try:
                l = len(test_data[0])
                predict_1 = model_1.predict(test_data)
        # =============================================================================
        #         predict_2 = model_2.predict(test_data)
        #         predict_3 = model_3.predict(test_data)
        #         predict_4 = model_4.predict(test_data)
        # =============================================================================
                pred = predict_1[0]
                #print(pred)
                pred0 = list(pred)
                #print(classes[pred0.index(max(pred0))])
                confidence = round(max(pred0)*100, 2)
                label = classes[pred0.index(max(pred0))]
                if confidence<50 and label=="Happy":
                    new_list = pred0[1:]
                    new_classes = classes[1:]
                    confidence = round((max(new_list)/(sum(new_list)))*100, 2)
                    label = new_classes[new_list.index(max(new_list))]
            
                cv2.putText(img, label + ": " + str(confidence) + "%", (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                ensemble.append(label)
            except:
                None
        else:
            try:
                cv2.putText(img, label + ": " + str(confidence) + "%", (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            except:
                None
        cv2.imshow("Image", img)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyWindow("Image")
    ensemble = np.array(ensemble)
    #print(ensemble)
    emotions = {"Happy": 0, "Sad": 0, "Neither": 0}
    for i in ensemble:
        emotions[i] += 1
        
    Total = sum(list(emotions.values()))
    emotions["Happy"] /= Total
    emotions["Sad"] /= Total
    emotions["Neither"] /= Total
    
    print("You were happy {}% of the time, sad {}% of the time, and neither happy nor sad {}% of the time".format(round(emotions["Happy"]*100, 2), round(emotions["Sad"]*100, 2), round(emotions["Neither"]*100, 2)))
    
    
    addsongs(int(emotions["Happy"]*100))
    
    #return emotions

 

root= tk.Tk()
root.title("Welcome to Song4U!")

canvas=tk.Canvas(root, width=400, height=100)
canvas.grid(columnspan=3)

logo=Image.open("/Users/saathvikdirisala/Downloads/Python/Logo.png")
logo= ImageTk.PhotoImage(logo)
logoFinal=tk.Label(image=logo)
logoFinal.image= logo
logoFinal.grid(column=0,row=0)


#Bottom message
message= tk.Label(root,text= "Please enter the redirected URL", font="calibri")
message.grid(columnspan=3,column=0,row=1)

#Text box
# =============================================================================
# 
# textbox= tk.Text(root, height=10, width=60)
# textbox.grid(row=0,column=1)
# =============================================================================

# =============================================================================
# 
# def retrieve_input():
#     input=textbox.get(1.0,tk.END)
#     #print(input)
#     f = open("/Users/saathvikdirisala/Downloads/Python/API/temp.txt", "w")
#     f.write(input)
#     f.close()
# =============================================================================
    

# =============================================================================
# button1= tk.Button(root,text="Authorize URL", command= lambda: retrieve_input())
# button1.place(x=1025,y=500)
# =============================================================================


# def Open_Cam():
#     cap=cv2.VideoCapture(0)
#     i=0
#     while i<250:
#         success,img=cap.read()
#         cv2.imshow("Image",img)
#         cv2.waitKey(1)
#         i+=1
#     cv2.destroyWindow('Image')
      
    

# def Close_Cam():
#     try:
#         cv2.destroyWindow('Image')
#     except:
#         None


button2= tk.Button(root,text="Open Camera", bg = "#000000", command=lambda: openCamera(LoadModel()))
button2.place(x=1025,y=200)

# button3= tk.Button(root,text="Close Camera", command= Close_Cam)
# button3.place(x=1025,y=250)

root.mainloop()


