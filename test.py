# encoding=utf8

import json
# import urllib
import urllib.parse
import urllib.request
import urllib.error

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from PIL import Image
import requests

from io import BytesIO

from itertools import chain, combinations

import imp
# imp.reload

import sys
imp.reload(sys)
# sys.setdefaultencoding('utf8')

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def subsets(s):
    return map(set, powerset(s))

def common_elements(list1, list2):
	return list(set(list1) & set(list2))

def different_elements(list1, list2):
	return list(set(list2) - set(list1))

def generateRecipes(ingredients):
	cred = credentials.Certificate('demotesterito-2e621f253c03.json')
	firebase_admin.initialize_app(cred, {'projectId': 'demotesterito',})
	db = firestore.client()

	sets = subsets(ingredients) # get different combinations of ingredients
	i = 0
	invalidCount = 0
	for theSet in sets:
		pageNumber = 1
		#no point if only 2 ingredients
		if len(theSet) < 3:
			continue
		ing = ",".join(theSet)
		while(pageNumber < 6): #60 results
			tempUrl = url + urllib.parse.urlencode({"i":ing,"p":pageNumber})
			try:
				response = requests.get(tempUrl).json()
				i = i + 1
				for j in range(len(response['results'])):
					name =  response['results'][j]['title']
					href = response['results'][j]['href']
					ingr = list((response['results'][j]['ingredients']).strip().split(', '))
					common = common_elements(ingredients,ingr)
					different = different_elements(ingredients,ingr)
					if(len(different) == 0): #no missing ingredients
						#access firestore
						doc_ref = db.collection(u'Recipes').document(name)
						doc_ref.set({
						    u'name': name,
						    u'url': href,
						    u'ingredients': ingr,
						    u'Missing Ingredients': different,
						    u'Common Ingredients': common
						})
			except ValueError as e: #random json encoding error
				invalidCount = invalidCount + 1
			pageNumber = pageNumber + 1
	#print i # number of api calls

#Working version on one time use. Change url in image to test
app = ClarifaiApp(api_key='bc65f5c343c545fe9c8927cf054622b4')
model = app.models.get('food-items-v1.0')

#Crop the image
response = requests.get("https://firebasestorage.googleapis.com/v0/b/demotesterito.appspot.com/o/Photos%2F19908?alt=media&token=ed32ff86-063d-4934-b193-30c1e76aa95b")
start = Image.open(BytesIO(response.content))
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
			if(response["outputs"][0]["data"]["concepts"][i]['name'] not in results):
				results.append(response["outputs"][0]["data"]["concepts"][i]['name'])

# for i in results:
# 	print(i)

ingredients = []
for i in results:
	ingredients.append(i)
url = 'http://www.recipepuppy.com/api/?'

generateRecipes(ingredients)