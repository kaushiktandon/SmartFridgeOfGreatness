from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import json

#Working version on one time use. Change url in image to test
app = ClarifaiApp(api_key='bc65f5c343c545fe9c8927cf054622b4')
model = app.models.get('food-items-v1.0')
image = ClImage(url='https://upload.wikimedia.org/wikipedia/commons/0/0e/Milk_glass.jpg')
response = model.predict([image])
size = len(response["outputs"][0]["data"]["concepts"])
for i in range(size):
	if(response["outputs"][0]["data"]["concepts"][i]['value'] > .99):
		print response["outputs"][0]["data"]["concepts"][i]['name'], response["outputs"][0]["data"]["concepts"][i]['value']

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
				print response["outputs"][0]["data"]["concepts"][i]['name'], response["outputs"][0]["data"]["concepts"][i]['value']
				ingredients.append(response["outputs"][0]["data"]["concepts"][i]['name'])
	return ingredients