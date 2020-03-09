import sys
from bs4 import BeautifulSoup  # Web scraping
from urllib.request import Request
from urllib.request import urlopen as urlReq  # Open URLs
import concurrent.futures  # Thread pool

def getRecipeList(recipeUrl):
    # Opening the connection grabing webpage, store all raw information
    req = Request(recipeUrl, headers={'User-Agent': 'Mozilla/5.0'})
    uClient = urlReq(req)
    htmlRaw = uClient.read()
    uClient.close()

    # Parse raw HTML
    soup = BeautifulSoup(htmlRaw, "html.parser")

    recipeCard = {}

    # Store URL into recipe card
    recipeCard['URL'] = recipeUrl

    # Find title and store into recipe card
    recipeTitle = soup.find("h1", {"class": "entry-title"}).text
    recipeCard['title'] = recipeTitle

    # Find image URL store into recipe card.
    imageContainer = soup.find("div", {"class", "featured-image"})
    imageUrl = imageContainer.img['src']
    recipeCard['image'] = imageUrl

    # Return single recipe
    return recipeCard

def getUrls(item, pageNum):
    # Search a few pages from main search result
    searchUrl = "https://www.simplyrecipes.com/recipes/main-ingredient/" + item + "/page/" + str(pageNum) + "/"
    
    req = Request(searchUrl, headers={'User-Agent': 'Mozilla/5.0'})
    recipeUrlList = urlReq(req)
    htmlRaw = recipeUrlList.read()
    recipeUrlList.close()
    soup = BeautifulSoup(htmlRaw, "html.parser")

    # Find all recipe URLs and return URL list
    recipeUrlList = []
    recipeBlockContainer = soup.findAll("h2", {"class": "grd-title-link"})
    for recipeBlock in recipeBlockContainer:
        recipeUrl = recipeBlock.a['href']
        recipeUrlList.append(recipeUrl)

    return recipeUrlList


def get_simply_recipe(recipeUrl):
    # Opening the connection grabing webpage, store all raw information
    req = Request(recipeUrl, headers={'User-Agent': 'Mozilla/5.0'})
    uClient = urlReq(req)
    htmlRaw = uClient.read()
    uClient.close()

    # Parse raw HTML
    soup = BeautifulSoup(htmlRaw, "html.parser")

    recipeCard = {}

    # Store site name into recipe card
    recipeCard['siteName'] = "Simply Recipes"

    # Store URL into recipe card
    recipeCard['URL'] = recipeUrl

    # Find title and store into recipe card
    recipeTitle = soup.find("h1", {"class": "entry-title"}).text
    recipeCard['title'] = recipeTitle

    # Find image URL store into recipe card.
    imageContainer = soup.find("div", {"class", "featured-image"})
    imageUrl = imageContainer.img['src']
    recipeCard['image'] = imageUrl

    # Find metadata of the recipe
    metadataAry = []
    recipePrep = soup.find("li", {"class": "recipe-prep"}).text.strip()
    recipeCook = soup.find("li", {"class": "recipe-cook"}).text.strip()
    recipeYield = soup.find("li", {"class": "recipe-yield"}).text.strip()
    metadataAry.append(recipePrep)
    metadataAry.append(recipeCook)
    metadataAry.append(recipeYield)
    recipeCard['metadata'] = metadataAry

    # Find ingredients
    ingredientListAry = []
    ingredientList = soup.findAll("li", {"class": "ingredient"})
    for ingredientItem in ingredientList:
        ingredient = ingredientItem.text
        ingredientListAry.append(ingredient)
    recipeCard['ingredients'] = ingredientListAry

    # Find Instructions
    instructionsAry = []
    instructionsContainer = soup.find("div", {"id": "sr-recipe-method"})
    instructions = instructionsContainer.findAll("p")
    for instructionItem in instructions:
        instruction = instructionItem.text.strip()
        instructionsAry.append(instruction)
    recipeCard['instructions'] = instructionsAry

    # Return single recipe
    return recipeCard


def simply_recipes_search(searchAry):
    recipe_dict = {}
    for item in searchAry:
        pass
    # Get a list of recipe URLs from main search page
    recipeUrlList = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(getUrls, searchAry[0], page) for page in
                    range(1,4)]  ##### Number of pages to search
        for f in concurrent.futures.as_completed(results):
            recipeUrlList = recipeUrlList + f.result()

    # Get a recipes from a list of URLs
    recipeBook = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(getRecipeList, recipeUrl) for recipeUrl in recipeUrlList]
        for f in concurrent.futures.as_completed(results):
            recipeBook.append(f.result())

    recipe_dict['simply_recipes'] = recipeBook

    return recipe_dict
