import json
import requests
import urllib

ingredients = ['onions','garlic','milk','eggs','ham','cheese']
url = 'http://www.recipepuppy.com/api/?'

class Recipe:
	def __init__(self,name,url,ingredients,numInCommon,numMissing):
		self.name = name
		self.url = url
		self.ingredients = ingredients
		self.numInCommon = numInCommon
		self.numMissing = numMissing


from itertools import chain, combinations
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def subsets(s):
    return map(set, powerset(s))

def common_elements(list1, list2):
	return list(set(list1) & set(list2))

sets = subsets(ingredients) # get different combinations of ingredients
#only want to use if at least 2 ingredients are used
i = 0
recipes = list()
for theSet in sets:
	#if len(theSet) < 2:
	#	i = i + 1
	#	continue
	#print theSet
	if i < len(sets)-1:
		i = i + 1
		continue
	ing = ",".join(theSet)
	tempUrl = url + urllib.urlencode({"i":ing})
	print tempUrl
	response = requests.get(tempUrl).json()
	for j in range(1):#len(response['results'])):
		name =  response['results'][j]['title']
		url = response['results'][j]['href']
		ingr = list(str(response['results'][j]['ingredients']).replace(' ','').split(','))
		common = common_elements(ingredients,ingr)
		recipes.append(Recipe(name,url,ingr,len(common),len(ingredients)-len(common)))		
	i = i + 1
