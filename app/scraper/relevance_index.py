def calc_relevance(search_list, ingredients):
    match_list = []

    for item in search_list:
        for ingredient in ingredients:
            if ingredient.find(item) != -1:
                match_list.append(item)

    match_list = list(set(match_list))
    match_index = int(len(match_list)/len(search_list)) * 100

    return match_index
