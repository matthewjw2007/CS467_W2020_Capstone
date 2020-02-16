import sys
from bs4 import BeautifulSoup # Web scraping 
from urllib.request import urlopen as urlReq # Open URLs
import concurrent.futures # Thread pool
from relevanceIndex import calcRelevance

import time # timing the amount of time required to search
import pprint # Pretty Print to make things print neatly

def getUrls(item, pageNum):
	# Search a few pages from main search result
	searchUrl = "https://www.allrecipes.com/search/results/?wt=" + item + "&page=" + str(pageNum)
	recipeUrlList = urlReq(searchUrl)
	htmlRaw = recipeUrlList.read()
	recipeUrlList.close()
	soup = BeautifulSoup(htmlRaw, "html.parser")

	# Find all recipe URLs and return URL list
	recipeUrlList = []
	recipeBlockContainer = soup.findAll("article", {"class":"fixed-recipe-card"})
	for recipeBlock in recipeBlockContainer:
		recipeUrl = recipeBlock.div.a['href']
		recipeUrlList.append(recipeUrl)

	return recipeUrlList


def getRecipe(recipeUrl, searchAry):
	# Opening the connection grabing webpage, store all raw information
	uClient = urlReq(recipeUrl)
	htmlRaw = uClient.read()
	uClient.close()

	# Parse raw HTML 
	soup = BeautifulSoup(htmlRaw, "html.parser")

	recipeCard = {}

	# Store site name into recipe card
	recipeCard['siteName'] = "All Recipes"

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
	recipeMetadata = soup.findAll("div", {"class":"recipe-meta-item"})
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

	# Find percentage match
	percentMatch = calcRelevance(searchAry, ingredientListAry)
	recipeCard['percentMatch'] = percentMatch

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

	# Return single recipe
	return recipeCard


def allRecipeSearch(searchAry):

	# Get a list of recipe URLs from main search page
	recipeUrlList = []
	with concurrent.futures.ProcessPoolExecutor() as executor:
		results = [executor.submit(getUrls, searchAry[0], page) for page in range(2)] ##### Number of pages to search
		for f in concurrent.futures.as_completed(results):
			recipeUrlList = recipeUrlList + f.result()

	# Get a recipes from a list of URLs
	recipeBook = []
	with concurrent.futures.ProcessPoolExecutor() as executor:
		results = [executor.submit(getRecipe, recipeUrl, searchAry) for recipeUrl in recipeUrlList]
		for f in concurrent.futures.as_completed(results):
			recipeBook.append(f.result())

	return(recipeBook)