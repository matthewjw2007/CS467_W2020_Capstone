import sys
from bs4 import BeautifulSoup # Web scraping 
from urllib.request import urlopen as urlReq  # Open URLs
import concurrent.futures # Thread pool
import pprint # Pretty Print to make things print neatly
import time
from .all_recipes import allrecipe_search  # importing search function from all_recipes.py
from .food_network import food_network_search


def recipe_search(ingredients, websites):
	print(websites)

	main_dict = {}

	# Start timer
	start = time.perf_counter()

	# Searching sites with multiprocessing
	with concurrent.futures.ProcessPoolExecutor() as executor:
		if 'allrecipes' in websites:
			all_recipe_dict = executor.submit(allrecipe_search, ingredients)
			# Since submit returns a future object and not the result of the function, we need to call .result
			main_dict.update(all_recipe_dict.result())
		if 'foodnetwork' in websites:
			food_network_dict = executor.submit(food_network_search, ingredients)
			main_dict.update(food_network_dict.result())

	# Stop timer
	finish = time.perf_counter()

	total_time = round(finish-start, 2)

	# Calculate search time
	print("Total Search Time: " + str(total_time) + " seconds")

	return main_dict
