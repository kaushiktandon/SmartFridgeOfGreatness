from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from PIL import Image
import json

#Working version on one time use. Change url in image to test
app = ClarifaiApp(api_key='bc65f5c343c545fe9c8927cf054622b4')
model = app.models.get('food-items-v1.0')
# image = ClImage('testFridge.jpg')

#Crop the image
start = Image.open("testFridge.jpg")
first = start.crop((0, 0, 1088, 1224))
first.save("item1.jpg")
second = start.crop((1088,0, 2176, 1224))
second.save("item2.jpg")
third = start.crop((2176, 0, 3264, 1224))
third.save("item3.jpg")
fourth = start.crop((0, 1224, 1088, 2448))
fourth.save("item4.jpg")
fifth = start.crop((1088, 1224, 2176, 2448))
fifth.save("item5.jpg")
sixth = start.crop((2176, 1224, 3264, 2448))
sixth.save("item6.jpg")

item1 = ClImage(("item1.jpg"))
item2 = ClImage(("item2.jpg"))
item3 = ClImage(("item3.jpg"))
item4 = ClImage(("item4.jpg"))
item5 = ClImage(("item5.jpg"))
item6 = ClImage(("item6.jpg"))

# response = model.predict([image])
response = model.predict([item1, item2, item3, item4, item5, item6])
size = len(response["outputs"][0]["data"]["concepts"])
for i in range(size):
	if(response["outputs"][0]["data"]["concepts"][i]['value'] > .99):
		print("poo")
		print(response["outputs"][0]["data"]["concepts"][i]['name'], response["outputs"][0]["data"]["concepts"][i]['value'])

#firebase version - photos should be a list of file locations or something
def processPhoto(photos):
	app = ClarifaiApp(api_key='bc65f5c343c545fe9c8927cf054622b4')
	model = app.models.get('food-items-v1.0')
	ingredients = [];
	for photo in photos:
		image = ClImage(file_obj=open(photo));#('/home/user/image.jpeg', 'rb'))
		response = model.predict([image])
		size = len(response["outputs"][0]["data"]["concepts"])
		for i in range(size):
			if(response["outputs"][0]["data"]["concepts"][i]['value'] > .99):
				print(response["outputs"][0]["data"]["concepts"][i]['name'], response["outputs"][0]["data"]["concepts"][i]['value'])
				ingredients.append(response["outputs"][0]["data"]["concepts"][i]['name'])
	return ingredients