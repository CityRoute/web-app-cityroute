import requests
import json
import os

file_landmarks = open(os.getcwd()+'\\src\\assets\\landmarks.json', "r")

landmarks_data = json.load(file_landmarks)


for count, landmark in enumerate(landmarks_data['markers']):
    print(count, landmark['address'])
    string = f"https://maps.googleapis.com/maps/api/streetview?size=400x400&location={landmark['address']}&key=AIzaSyBDqRNi_Umchyewenecd7Ly8sFkPk_gxHc"
    response = requests.get(string)
    
    image_file = open(os.getcwd()+f"\\scripts\\{landmark['address']}.png", "wb")
    image_file.write(response.content)
    image_file.close()
    break
