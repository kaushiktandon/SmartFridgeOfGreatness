# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


import json
import requests
import urllib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

ingredients = [u'rice',u'lettuce',u'milk',u'garlic',u'chicken',u'cheese',u'onion']
url = 'http://www.recipepuppy.com/api/?'

class Recipe:
	def __init__(self,name,url,ingredients,commonIngredients,missingIngredients):
		self.name = name
		self.url = url
		self.ingredients = ingredients
		self.commonIngredients = commonIngredients
		self.missingIngredients = missingIngredients
	def __repr__(self):
		return u'Recipe(name={}, url={}, ingredients={}, commonIngredients={}, missingIngredients={})'.format(
            self.name, self.url, self.ingredients, self.commonIngredients, self.missingIngredients)
	def to_dict(self):
		dest = {
			u'name':self.name,
			u'url':self.url,
			u'ingredients':self.ingredients,
			u'commonIngredients':self.commonIngredients,
			u'missingIngredients':self.missingIngredients
		}
		return dest


from itertools import chain, combinations
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
	cred = credentials.Certificate('/Users/kaush/SmartFridgeOfGreatness/demotesterito-2e621f253c03.json')
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
			tempUrl = url + urllib.urlencode({"i":ing,"p":pageNumber})
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
			except ValueError, e: #random json encoding error
				invalidCount = invalidCount + 1
			pageNumber = pageNumber + 1
	#print i # number of api calls

generateRecipes(ingredients)


#db.collection(u'Recipes').add(recipes[0].to_dict())
#doc_ref.set({
#    u'name': u'Ada',
#    u'url': u'espn.go.com',
#    u'ingredients': ingredients,
#    u'Missing Ingredients': ingredients,
#    u'Common Ingredients': ingredients
#})