import json
import requests
import urllib

ingredients = ['onions','garlic','milk','eggs','ham','cheese']
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

def getRecipes(ingredients):
	sets = subsets(ingredients) # get different combinations of ingredients
	recipes = list()
	pageNumber = 1
	i = 0
	for theSet in sets:
		#no point if only one ingredient
		if len(theSet) < 2:
			i = i+1
			continue
		if i < len(sets)-1:
			i = i + 1
			continue
		ing = ",".join(theSet)
		if(pageNumber == 1):#while(pageNumber < 5):
			tempUrl = url + urllib.urlencode({"i":ing,"p":pageNumber})
			response = requests.get(tempUrl).json()
			for j in range(len(response['results'])):
				name =  response['results'][j]['title']
				href = response['results'][j]['href']
				ingr = list(str(response['results'][j]['ingredients']).replace(' ','').split(','))
				common = common_elements(ingredients,ingr)
				different = different_elements(ingredients,ingr)
				print len(common), len(different), name, href
				recipes.append(Recipe(name,href,ingr,common,different))
			pageNumber = pageNumber + 1
		i = i + 1
	return recipes

recipes = getRecipes(ingredients)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
#cred = credentials.ApplicationDefault()
cred = credentials.Certificate('/Users/kaush/SmartFridgeOfGreatness/demotesterito-2e621f253c03.json')

firebase_admin.initialize_app(cred, {
  'projectId': 'demotesterito',
})


db = firestore.client()
doc_ref = db.collection(u'Recipes').document(u'alovelace')
#db.collection(u'Recipes').add(recipes[0].to_dict())
doc_ref.set({
#    u'name': u'Ada',
#    u'url': u'espn.go.com',
#    u'ingredients': [{'a','b'}]
#    u'Missing Ingredients': ingredients,
#    u'Common Ingredients': ingredients
})