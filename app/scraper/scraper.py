import sys
from bs4 import BeautifulSoup # Web scraping 
from urllib.request import urlopen as urlReq # Open URLs
import concurrent.futures # Thread pool

import pprint # Pretty Print to make things print neatly

import time


def get_recipe(recipeUrl):
	# Opening the connection grabbing webpage, store all raw information
	uClient = urlReq(recipeUrl)
	htmlRaw = uClient.read()
	uClient.close()

	# Parse raw HTML 
	soup = BeautifulSoup(htmlRaw, "html.parser")

	recipeCard = {}

	# Store URL into recipe card
	recipeCard['URL'] = recipeUrl

	# Find title and store into recipe card
	recipeTitle = soup.find("h1").text
	recipeCard['title'] = recipeTitle

	# Find image URL store into recipe card. 
	imageContainer = soup.find("div", {"class", "image-container"})
	if imageContainer:
		imageUrl = imageContainer.div['data-src']
	else:
		imageContainer = soup.find("img", {"class", "rec-photo"})
		imageUrl = imageContainer['src']
	recipeCard['image'] = imageUrl

	# Find metadata of the recipe
	metadataAry = []
	recipeMetadata = soup.findAll("div", {"class": "recipe-meta-item"})
	if recipeMetadata:
		for metadata in recipeMetadata:
			metadataHeader = metadata.find("div", {"class", "recipe-meta-item-header"}).text.strip()
			metadataBody = metadata.find("div", {"class", "recipe-meta-item-body"}).text.strip()
			metadataEntry = metadataHeader + ' ' + metadataBody
			metadataAry.append(metadataEntry)
	else:
		recipeMetadata = soup.findAll("li",{"aria-label":True})
		for metadata in recipeMetadata:
			metadataEntry = metadata['aria-label']
			metadataAry.append(metadataEntry)
	recipeCard['metadata'] = metadataAry

	# Find ingredients
	ingredientListAry = []
	ingredientList = soup.findAll("li", {"class":"ingredients-item"})
	if ingredientList:
		for ingredientItem in ingredientList:
			ingredient = ingredientItem.find("span", {"class":"ingredients-item-name"}).text.strip()
			ingredientListAry.append(ingredient)
	else:
		ingredientList = soup.findAll("label", {"title":True})
		for ingredientItem in ingredientList:
			ingredient = ingredientItem['title']
			ingredientListAry.append(ingredient)
	recipeCard['ingredients'] = ingredientListAry

	# Find Instructions
	instructionsAry = []
	instructionsContainer = soup.findAll("li",{"class":"subcontainer instructions-section-item"})
	if instructionsContainer:
		for instructionItem in instructionsContainer:
			instruction = instructionItem.p.text
			instructionsAry.append(instruction)
	else:
		instructionsContainer = soup.findAll("span",{"class":"recipe-directions__list--item"})
		for instructionItem in instructionsContainer:
			instruction = instructionItem.text.strip()
			instructionsAry.append(instruction)
	recipeCard['instructions'] = instructionsAry

	# Return single recipe as dictionary
	return recipeCard


def recipe_search(ingredients):

	recipeDict = {}

	ingredientDict = {}

	# print (f"Contents of recipe_search input: {ingredients}")

	# Search for individual ingredients
	for item in ingredients:

		# Search a list of recipes on all recipe.com
		searchUrl = "https://www.allrecipes.com/search/results/?wt=" + item
		recipeUrlList = urlReq(searchUrl)
		htmlRaw = recipeUrlList.read()
		recipeUrlList.close()

		soup = BeautifulSoup(htmlRaw, "html.parser")

		recipeBook = []

		# Git a list of recipes from main search result page
		recipeUrlList = []
		recipeBlockContainer = soup.findAll("article", {"class": "fixed-recipe-card"})
		for recipeBlock in recipeBlockContainer:
			recipeUrl = recipeBlock.div.a['href']
			recipeUrlList.append(recipeUrl)
			
		with concurrent.futures.ThreadPoolExecutor() as executor:
			results = [executor.submit(get_recipe, recipeUrl) for recipeUrl in recipeUrlList]
			for f in concurrent.futures.as_completed(results):
				recipeBook.append(f.result())

		ingredientDict[item] = recipeBook

	recipeDict['allrecipes'] = ingredientDict

	return recipeDict
