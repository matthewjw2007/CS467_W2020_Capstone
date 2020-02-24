import sys
from bs4 import BeautifulSoup  # Web scraping
from urllib.request import urlopen as urlReq  # Open URLs
import concurrent.futures  # Thread pool

from .relevance_index import calc_relevance

import time  # timing the amount of time required to search
import pprint  # Pretty Print to make things print neatly


def getRecipeList(recipeUrl):
    # Opening the connection grabing webpage, store all raw information
    uClient = urlReq(recipeUrl)
    htmlRaw = uClient.read()
    uClient.close()

    # Parse raw HTML
    soup = BeautifulSoup(htmlRaw, "html.parser")

    recipeCard = {}

    # Store URL into recipe card
    recipeCard['URL'] = recipeUrl

    # Find title and store into recipe card
    recipeTitle = soup.find("span", {"class": "o-AssetTitle__a-HeadlineText"}).text
    recipeCard['title'] = recipeTitle

    # Find star rating and store into recipe card
    recipe_stars = soup.find("span", {"class": "gig-rating-stars"})["title"]
    recipeCard['stars'] = recipe_stars

    # Find image URL store into recipe card.
    imageContainer = soup.find("img", {"class", "m-MediaBlock__a-Image a-Image"})
    if imageContainer:
        imageUrl = imageContainer['src']
        recipeCard['image'] = imageUrl
    else:
        recipeCard['image'] = ""

    # Return single recipe
    return recipeCard


def getUrls(item, pageNum):
    # Search a few pages from main search result
    searchUrl = "https://www.foodnetwork.com/search/" + item + "-/p/" + str(pageNum) + "/rating"
    recipeUrlList = urlReq(searchUrl)
    htmlRaw = recipeUrlList.read()
    recipeUrlList.close()
    soup = BeautifulSoup(htmlRaw, "html.parser")

    # Find all recipe URLs and return URL list
    recipeUrlList = []
    recipeBlockContainer = soup.findAll("h3", {"class": "m-MediaBlock__a-Headline"})
    for recipeBlock in recipeBlockContainer:
        recipeUrl = "https:" + recipeBlock.a['href']
        if (not ("videos" in recipeUrl)):
            recipeUrlList.append(recipeUrl)

    return recipeUrlList


def get_foodnetwork(recipeUrl):
    # Opening the connection grabbing web page, store all raw information
    uClient = urlReq(recipeUrl)
    htmlRaw = uClient.read()
    uClient.close()

    # Parse raw HTML
    soup = BeautifulSoup(htmlRaw, "html.parser")

    recipeCard = {}

    # Store site name into recipe card
    recipeCard['siteName'] = "Food Network"

    # Store URL into recipe card
    recipeCard['URL'] = recipeUrl

    # Find title and store into recipe card
    recipeTitle = soup.find("span", {"class": "o-AssetTitle__a-HeadlineText"}).text
    recipeCard['title'] = recipeTitle

    # Find image URL store into recipe card.
    imageContainer = soup.find("img", {"class", "m-MediaBlock__a-Image a-Image"})
    imageUrl = imageContainer['src']
    recipeCard['image'] = imageUrl

    # if imageContainer:
    #     imageUrl = imageContainer['src']
    #     recipeCard['image'] = imageUrl
    # else:
    #     recipeCard['image'] = ""

    # Find metadata of the recipe
    metadataAry = []
    levelInfo = soup.find("div", {"class": "o-RecipeInfo"})
    itemsInfo = levelInfo.findAll("li")
    for item in itemsInfo[:5]:
        item = item.text.replace('\n', ' ').strip()
        metadataAry.append(item)
    recipeCard['metadata'] = metadataAry

    # Find ingredients
    ingredientListAry = []
    ingredientList = soup.findAll("p", {"class": "o-Ingredients__a-Ingredient"})
    for ingredientItem in ingredientList:
        ingredient = ingredientItem.text
        ingredientListAry.append(ingredient)
    recipeCard['ingredients'] = ingredientListAry

    # # Find percentage match
    # percentMatch = calc_relevance(searchAry, ingredientListAry)
    # recipeCard['percentMatch'] = percentMatch

    # Find Instructions
    instructionsAry = []
    instructionsContainer = soup.findAll("li", {"class": "o-Method__m-Step"})
    for instructionItem in instructionsContainer:
        instruction = instructionItem.text.strip()
        instructionsAry.append(instruction)
    recipeCard['instructions'] = instructionsAry

    # Return single recipe
    return recipeCard


def food_network_search(ingredients):
    recipe_dict = {}
    # Get a list of recipe URLs from main search page
    recipeUrlList = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(getUrls, ingredients, page) for page in
                    range(1,3)]  ##### Number of pages to search
        for f in concurrent.futures.as_completed(results):
            recipeUrlList = recipeUrlList + f.result()

    # Get a recipes from a list of URLs
    recipeBook = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(getRecipeList, recipeUrl) for recipeUrl in recipeUrlList]
        for f in concurrent.futures.as_completed(results):
            recipeBook.append(f.result())

    recipe_dict['food_network'] = recipeBook

    return recipe_dict
