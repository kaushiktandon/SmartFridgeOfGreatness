# encoding=utf8

from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from PIL import Image
import requests
from io import BytesIO
import json

#Working version on one time use. Change url in image to test
app = ClarifaiApp(api_key='bc65f5c343c545fe9c8927cf054622b4')
model = app.models.get('food-items-v1.0')

#Crop the image
response = requests.get("https://firebasestorage.googleapis.com/v0/b/demotesterito.appspot.com/o/Photos%2F19908?alt=media&token=ed32ff86-063d-4934-b193-30c1e76aa95b")
start = Image.open(BytesIO(response.content))

first = start.crop((0, 0, 816, 1632))
first.save("item1.jpg")
second = start.crop((816,0, 1632, 1632))
second.save("item2.jpg")
third = start.crop((1632, 0, 2448, 1632))
third.save("item3.jpg")
fourth = start.crop((0, 1632, 816, 3264))
fourth.save("item4.jpg")
fifth = start.crop((816, 1632, 1632, 3264))
fifth.save("item5.jpg")
sixth = start.crop((1632, 1632, 2448, 3264))
sixth.save("item6.jpg")

item1 = ClImage(filename="item1.jpg")
item2 = ClImage(filename="item2.jpg")
item3 = ClImage(filename="item3.jpg")
item4 = ClImage(filename="item4.jpg")
item5 = ClImage(filename="item5.jpg")
item6 = ClImage(filename="item6.jpg")

fridge = [item1, item2, item3, item4, item5, item6]
results = []

for item in fridge:
	response = model.predict([item])
	size = len(response["outputs"][0]["data"]["concepts"])
	for i in range(size):
		if(response["outputs"][0]["data"]["concepts"][i]['value'] > .95):
			if(response["outputs"][0]["data"]["concepts"][i]['name'] not in results and str(response["outputs"][0]["data"]["concepts"][i]["name"]) != "chocolate"):
				results.append(response["outputs"][0]["data"]["concepts"][i]['name'])

# for i in results:
# 	print(i)