import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen as urlReq
import json
import time


def getRecipe(recipeUrl, data):
	# Opening the connection grabing webpage, store all raw information
	uClient = urlReq(recipeUrl)
	htmlRaw = uClient.read()
	uClient.close()

	# Parse raw HTML 
	soup = BeautifulSoup(htmlRaw, "html.parser")

	recipeDict = {}

	# Find title
	recipeTitle = soup.find("h1", {"class":"headline heading-content"}).text
	# beef: class=recipe-summary__h1

	recipeDict['title'] = recipeTitle

	# Find metadata of the recipe
	recipeMetadata = soup.findAll("div", {"class":"recipe-meta-item"})
	metadataAry = []
	for metadata in recipeMetadata:
		metadataHeader = metadata.find("div", {"class", "recipe-meta-item-header"}).text.strip()
		metadataBody = metadata.find("div", {"class", "recipe-meta-item-body"}).text.strip()
		metadataAry.append({metadataHeader: metadataBody})
	recipeDict['metadata'] = metadataAry

	# Find ingredients
	ingredientList = soup.findAll("li", {"class":"ingredients-item"})
	ingredientListAry = []
	for ingredientItem in ingredientList:
		ingredient = ingredientItem.find("span", {"class":"ingredients-item-name"}).text.strip()
		ingredientListAry.append(ingredient)
	recipeDict['ingredients'] = ingredientListAry

	# Find Instructions
	InstructionsContainer = soup.findAll("li",{"class":"subcontainer instructions-section-item"})
	instructionsAry = []
	for instructionItem in InstructionsContainer:
		instruction = instructionItem.p.text
		instructionsAry.append(instruction)
	recipeDict['instructions'] = instructionsAry

	# Add the recipeDict to the data dict
	data.append(recipeDict)


if __name__ == "__main__":
	
	start_time = time.time()

	# Search a list of recipes on all recipe.com
	searchUrl = "https://www.allrecipes.com/search/results/?wt=" + sys.argv[1]
	recipeUrlList = urlReq(searchUrl)
	htmlRaw = recipeUrlList.read()
	recipeUrlList.close()

	soup = BeautifulSoup(htmlRaw, "html.parser")

	data = {'allrecipes': []}

	recipeCardContainer = soup.findAll("article", {"class":"fixed-recipe-card"})
	
	for recipeCard in recipeCardContainer:
		recipeUrl = recipeCard.div.a['href']
		getRecipe(recipeUrl, data['allrecipes'])

	print (data)
	print("--- %s seconds ---" % (time.time() - start_time))
