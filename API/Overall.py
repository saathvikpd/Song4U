import webbrowser
import requests
import json
import csv
import random
import os
from tkinter import *
from PIL import Image, ImageTk
import time

clientID = 'e46921ad8e01410abc08418d259f27a2'
clientSECRET = 'e20db8a2685342de9047477a47d94aa9'


def addsongs(threshold):

    threshold = threshold//10
    threshold_sad = 10 - threshold
    webbrowser.open("https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&scope=playlist-modify-private&redirect_uri=https://github.com/mohakvni/Song4U".format(CLIENT_ID = clientID))

    redirect = input("Input the redirected URL that you receive after authorization: ")
    temp = redirect.split("=")
    code_  = temp[1]

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'authorization_code',
        'client_id': clientID,
        'client_secret': clientSECRET, 
        'code' : code_,
        'redirect_uri' : 'https://github.com/mohakvni/Song4U'
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()


    access_token = auth_response_data['access_token']


    def get_UserID(code_):

        response = requests.get("https://api.spotify.com/v1/me", headers = {
            "Content-Type":"application/json","Authorization": "Bearer {token}".format(token=access_token)})

        content = response.json()
        return content["id"]


    headers = {"Content-Type":"application/json",
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    #os.chdir("API")

    f_happy= open ("./happy.csv","r")
    f_sad = open("./sad.csv","r")
    row_happy = csv.reader(f_happy)
    row_sad = csv.reader(f_sad)

    happy_list = []
    for i in row_happy:
      happy_list.append(i[1])

    sad_list = []
    for i in row_sad:
        sad_list.append(i[1])

    temp = random.randint(1,1000)
    hlist = happy_list[temp-threshold:temp]
    slist = sad_list[temp-threshold_sad:temp]
    overall = hlist + slist


    user_id = get_UserID(code_)

    endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    request_body = json.dumps({
              "name": "Mood",
              "description": "We created a playlist depending on if we think you are happy or sad",
              "public": False
            })
    response = requests.post(url = endpoint_url, data = request_body, headers= headers)
    playlist_id = response.json()['id']
    endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    request_body = json.dumps({
              "uris" : overall
            })
    response = requests.post(url = endpoint_url, data = request_body, headers= headers)
    if response.status_code == 201:
        print("We gotchya")
    else:
        print("Oops, there seems to be an error")
