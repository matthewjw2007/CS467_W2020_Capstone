import concurrent.futures # Thread pool


from .all_recipes import allrecipe_search  # importing search function from all_recipes.py
from .food_network import food_network_search
from .simply_recipes import simply_recipes_search

def recipe_search(ingredients, websites):
	main_dict = {}

	# Searching sites with multiprocessing
	with concurrent.futures.ProcessPoolExecutor() as executor:
		if 'allrecipes' in websites:
			query_string = ""
			for item in ingredients:
				query_string = query_string + item + '%20'
			# remove final '%20'
			query_string = query_string[:-3]
			# replace any space in string for searching
			if query_string.find(' '):
				query_string = query_string.replace(' ', '%20')
			all_recipe_dict = executor.submit(allrecipe_search, query_string)
			# Since submit returns a future object and not the result of the function, we need to call .result
			main_dict.update(all_recipe_dict.result())
		if 'foodnetwork' in websites:
			query_string = ""
			for item in ingredients:
				query_string = query_string + item + '-'
			query_string = query_string[:-1]
			if query_string.find(' '):
				query_string = query_string.replace(' ', '-')
			food_network_dict = executor.submit(food_network_search, query_string)
			main_dict.update(food_network_dict.result())
		if 'simplyRecipes' in websites:
			simply_recipes_search_dict = executor.submit(simply_recipes_search, ingredients)
			main_dict.update(simply_recipes_search_dict.result())

	return main_dict
