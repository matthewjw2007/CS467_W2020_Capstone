def calcRelevance(searchList, ingredients):
	matchList = [] 
	for item in searchList:
		for ingredient in ingredients:
			if (ingredient.find(item) != -1 ):
				matchList.append(item)

	matchList = list(set(matchList))
	matchIndex = int(len(matchList) / len(searchList) * 100)
	
	return matchIndex

	# def calcRelevance(list, ingredients):
	# matchNum = 0
	# for item in list:
	# 	for ingredient in ingredients:
	# 		if (ingredient.find(item) != -1 ):
	# 			matchNum += 1

	# matchIndex = int(matchNum / len(list) * 100)
	
	# return matchIndex