import sys
import concurrent.futures # Thread pool
import multiprocessing
from operator import itemgetter 

from allRecipe import allRecipeSearch
from foodNetwork import foodNetworkSearch

import time # timing the amount of time required to search
import pprint # Pretty Print to make things print neatly

##########################################################
# Search string
# Need modification to stitch into main program
searchString = "chicken, egg, flour, butter, sugar, soy sauce"
##########################################################

searchAry = searchString.split(', ')

# Start timer
start = time.perf_counter()

# Start searching sites by multiprocessing
with concurrent.futures.ProcessPoolExecutor() as executor:
    allRecipe = executor.submit(allRecipeSearch, searchAry)
    foodNetwork = executor.submit(foodNetworkSearch, searchAry)
    allRecipeBook = allRecipe.result()
    foodNetworkBook = foodNetwork.result()

# Start searching sites by serial processing
# allRecipeBook = allRecipeSearch(searchAry)
# foodNetworkBook = foodNetworkSearch(searchAry)

# End timer
finish = time.perf_counter()

recipeBook = allRecipeBook + foodNetworkBook
recipeBook = sorted(recipeBook, key=itemgetter('percentMatch'),reverse = True)

pprint.pprint(recipeBook)

print(f"Total search time: {round(finish-start, 2)} second(s)")

# NEED TO RETURN recipeBook later on